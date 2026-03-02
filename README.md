## AI Weather Assistant

### Project Overview

**AI Weather Assistant** is a small full‑stack demo that lets users ask natural‑language questions about current weather conditions.  
The system combines a React (Vite + TypeScript) frontend, a FastAPI + LangChain agent backend, and an MCP server that wraps the OpenWeather public REST API.

At a high level:
- The **frontend** shows a simple chat UI.
- The **agent backend** receives user messages, calls an OpenAI chat model with tools enabled, and returns a concise, plain‑text answer.
- The **MCP server** talks to the OpenWeather API and returns current weather data that the agent uses in its responses.

### High‑Level Architecture

- **React frontend (Vite + TypeScript)**  
  Renders a landing page and `ChatWindow` component, sends user messages to the agent backend at `http://localhost:8001/agent/chat`, and displays the assistant’s plain‑text replies.

- **Agent backend (FastAPI + LangChain + OpenAI)**  
  Exposes `/agent/chat`. It:
  - Adds a strict `SystemMessage` to enforce short, plain‑text, production‑ready answers.
  - Uses LangChain’s tool system to call `get_current_weather` when needed.
  - Orchestrates a short tool‑calling loop and returns the final, sanitized response to the frontend.

- **MCP server (FastAPI wrapper for OpenWeather)**  
  Runs on `http://localhost:8000`. It:
  - Reads an OpenWeather API key from environment variables.
  - Provides a simplified `/weather/current` endpoint that the agent’s tool calls instead of calling OpenWeather directly.

- **OpenWeather REST API**  
  Public third‑party service used as the actual data source for current weather conditions.

### Separation of Concerns

- **Frontend** focuses only on UI and user interaction: rendering chat bubbles, handling loading state, and calling a single HTTP endpoint.
- **Agent backend** owns all AI and reasoning logic: prompt formatting, tool‑calling, and post‑processing of LLM output.
- **MCP server** is a thin, independently deployable integration layer that:
  - Encapsulates the OpenWeather API contract.
  - Centralizes API‑key usage and error handling.
- **OpenWeather** remains an external dependency that can be swapped or extended without touching the frontend.

### MCP Wrapper Role

The MCP server:
- Normalizes the OpenWeather API into a stable internal shape.
- Keeps external API details (query params, units, base URL) out of the agent logic.
- Reads the OpenWeather API key from its own `.env`, so the key never leaves the backend environment.

### LLM Tool‑Calling Role

The agent backend:
- Exposes a LangChain tool `get_current_weather(city: str)` that calls the MCP server at `http://localhost:8000/weather/current`.
- Lets the OpenAI chat model decide when to call the tool based on user questions.
- Merges tool results back into a short, human‑readable answer, then sanitizes it to enforce:
  - Plain text (no markdown or bullets).
  - Fewer than 5 sentences.
  - Clear, concise phrasing.

## Environment Setup

### Prerequisites

- **Python**: recommended **3.11** (avoid 3.14+ for now due to ecosystem issues).
- **Node.js**: **18+** (Node 18 LTS or newer; Vite works well with 18 or 20).
- **npm** (bundled with Node) or **pnpm/yarn** if you prefer.

### Create and Activate a Python Virtual Environment

From the project root:

```bash
cd ai-weather-agent

# Create venv (using Python 3.11)
python -m venv .venv

# Activate on macOS / Linux
source .venv/bin/activate

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

You can also create separate virtual environments per service if you prefer, but a single shared one in the repo root is usually sufficient.

### Install Python Dependencies

There are two Python services, each with its own `requirements.txt`:

```bash
# From repo root, with venv activated:

cd mcp_server
pip install -r requirements.txt

cd ../agent_backend
pip install -r requirements.txt
```

### Install Frontend Dependencies

From the repo root:

```bash
cd frontend
npm install
```

## API Keys Setup

You need two API keys:
- **OpenWeather API key** for the MCP server.
- **OpenAI API key** for the agent backend.

### Obtain OpenWeather API Key

1. Go to the OpenWeather website and create an account.  
2. Generate an API key from your account dashboard.  
3. Copy the key; you will use it in the MCP server `.env`.

### Obtain OpenAI API Key

1. Sign in to your OpenAI account.  
2. Create an API key in the API keys section.  
3. Copy the key; you will use it in the agent backend `.env`.

### Where to Put `.env` Files

Create separate `.env` files for each backend service:

- `mcp_server/.env`
- `agent_backend/.env`

These files are **not** committed to git and are used only at runtime.

### Example `.env` Structures

**`mcp_server/.env`**

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

**`agent_backend/.env`**

```env
OPENAI_API_KEY=your_openai_api_key_here
```

You can add additional settings here as needed (e.g., logging flags, environment names).

## Running the Application

Open three terminals (or split panes), all from the project root (`ai-weather-agent`).

### 1. Start the MCP Server (port 8000)

```bash
cd mcp_server
uvicorn main:app --reload --port 8000
```

This exposes the internal weather endpoint at `http://localhost:8000/weather/current`.

### 2. Start the Agent Backend (port 8001)

In a new terminal:

```bash
cd agent_backend
uvicorn main:app --reload --port 8001
```

This exposes the chat endpoint at:

- `POST http://localhost:8001/agent/chat`
- Request body: `{"message": "What's the weather in London?"}`
- Response body: `{"response": "Short plain-text answer ..."}`  

The backend will:
- Call OpenAI with tool‑calling enabled.
- Use the MCP server to fetch current weather when needed.
- Return a short, plain‑text answer to the frontend.

### 3. Start the Frontend (port 5173)

In a third terminal:

```bash
cd frontend
npm run dev
```

Open your browser at `http://localhost:5173`.  
You will see the landing page; click **Get Started** to open the chat interface and start asking weather questions.

## Dependencies

- **Python services**
  - Each backend has a `requirements.txt`:
    - `mcp_server/requirements.txt`
    - `agent_backend/requirements.txt`
  - These include FastAPI, Uvicorn, LangChain, OpenAI client, and `requests` for HTTP calls.

- **Frontend**
  - The React app is managed via `frontend/package.json` and uses:
    - React + ReactDOM
    - Vite
    - TypeScript and related tooling

## Security Notes

- **API keys live only on the backend**:  
  - OpenWeather and OpenAI keys are stored in `.env` files for `mcp_server` and `agent_backend`.  
  - The React frontend **never** sees these keys; it talks only to `http://localhost:8001/agent/chat`.

- **`.env` files are ignored by git**:  
  - The repository’s `.gitignore` is configured so that `.env` files are not committed.  
  - Never paste your real keys into code or the README; always use environment variables.

- If you deploy this project, configure environment variables on your hosting platform instead of checking secrets into the repo.
