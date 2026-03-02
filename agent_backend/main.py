import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import re

load_dotenv()

from agent import get_current_weather

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System message defines strict formatting rules so the model
# aims for short, plain-text, production-friendly replies.
SYSTEM_MESSAGE = SystemMessage(
    content=(
        "You are a concise weather assistant for a production chat app. "
        "Follow these rules strictly: "
        "1) Respond in plain text only. Do NOT use markdown, bullet points, numbered lists, code blocks, or headings. "
        "2) Keep answers under 5 sentences. "
        "3) Use short, clear sentences that are easy to read. "
        "4) Do not add decorative characters or emojis."
    )
)


def _sanitize_plain_text(content: str, max_sentences: int = 5) -> str:
    """
    Enforce output formatting at the API boundary so that even if the model
    drifts from instructions, the user still receives plain, readable text.
    """
    text = content if isinstance(content, str) else str(content)

    # Strip common markdown/code markers so the UI never sees formatted output.
    text = text.replace("`", "")

    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        # Remove typical bullet prefixes (-, *, +) and simple numbered lists.
        if stripped.startswith(("- ", "* ", "+ ")):
            stripped = stripped[2:]
        stripped = re.sub(r"^\d+\.\s+", "", stripped)
        cleaned_lines.append(stripped)

    # Collapse into a single text block and normalize whitespace.
    text = " ".join(l for l in cleaned_lines if l.strip())
    text = " ".join(text.split())

    # Hard-cap the number of sentences for predictable, terse answers.
    sentences = re.split(r"(?<=[.!?])\s+", text)
    limited = " ".join(sentences[:max_sentences]).strip()
    return limited


llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
llm_with_tools = llm.bind_tools([get_current_weather])

tools_by_name = {t.name: t for t in [get_current_weather]}


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/agent/chat", response_model=ChatResponse)
def agent_chat(request: ChatRequest) -> ChatResponse:
    """Send a message to the agent and get a response (with tool use)."""
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is not set")

    # Always start each turn with the system message so formatting rules
    # are consistently applied, then add the latest user question.
    messages = [SYSTEM_MESSAGE, HumanMessage(content=request.message)]

    for _ in range(5):  # Maximum number of iterations
        result = llm_with_tools.invoke(messages)
        messages.append(result)

        if not getattr(result, "tool_calls", None):
            # Final guardrail: sanitize the raw model output to enforce
            # plain text, sentence limits, and readability before returning.
            clean = _sanitize_plain_text(result.content)
            return ChatResponse(response=clean)

        for tc in result.tool_calls:
            tool = tools_by_name.get(tc["name"])
            if not tool:
                messages.append(
                    ToolMessage(content=f"Unknown tool: {tc['name']}", tool_call_id=tc["id"])
                )
                continue
            output = tool.invoke(tc["args"])
            messages.append(ToolMessage(content=str(output), tool_call_id=tc["id"]))
