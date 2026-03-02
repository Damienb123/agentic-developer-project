export async function sendMessage(message: string): Promise<string> {
  try {
    const res = await fetch("http://localhost:8001/agent/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) {
      throw new Error(`Request failed with status ${res.status}`);
    }

    const data: { response: string } = await res.json();

    if (!data || typeof data.response !== "string") {
      throw new Error("Invalid response format from server");
    }

    return data.response;
  } catch (error) {
    console.error("Error sending message to agent:", error);
    throw error;
  }
}

