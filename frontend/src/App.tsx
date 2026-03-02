import React, { useState } from "react";
import { ChatWindow } from "./components/ChatWindow";

function App() {
  const [started, setStarted] = useState(false);

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background:
          "linear-gradient(135deg, rgba(59,130,246,0.12), rgba(96,165,250,0.18))",
        padding: "16px",
        boxSizing: "border-box",
      }}
    >
      {!started ? (
        <div
          style={{
            maxWidth: "480px",
            width: "100%",
            textAlign: "center",
            backgroundColor: "rgba(255,255,255,0.96)",
            borderRadius: "16px",
            padding: "32px 24px",
            boxShadow: "0 12px 30px rgba(15,23,42,0.15)",
            boxSizing: "border-box",
          }}
        >
          <h1
            style={{
              margin: 0,
              marginBottom: "12px",
              fontSize: "28px",
              fontWeight: 700,
              color: "#0f172a",
              letterSpacing: "0.02em",
            }}
          >
            AI Weather Assistant
          </h1>
          <p
            style={{
              margin: 0,
              marginBottom: "24px",
              fontSize: "15px",
              color: "#4b5563",
              lineHeight: 1.5,
            }}
          >
            Ask real-time weather questions powered by AI. Get clear, concise
            answers for any city in seconds.
          </p>
          <button
            type="button"
            onClick={() => setStarted(true)}
            style={{
              padding: "10px 20px",
              borderRadius: "999px",
              border: "none",
              backgroundColor: "#2563eb",
              color: "#ffffff",
              fontSize: "15px",
              fontWeight: 600,
              cursor: "pointer",
              boxShadow: "0 8px 20px rgba(37,99,235,0.3)",
              transition:
                "background-color 0.15s ease, transform 0.1s ease, box-shadow 0.15s ease",
            }}
            onMouseDown={(e) => {
              (e.currentTarget as HTMLButtonElement).style.transform =
                "translateY(1px)";
              (e.currentTarget as HTMLButtonElement).style.boxShadow =
                "0 4px 12px rgba(37,99,235,0.25)";
            }}
            onMouseUp={(e) => {
              (e.currentTarget as HTMLButtonElement).style.transform =
                "translateY(0)";
              (e.currentTarget as HTMLButtonElement).style.boxShadow =
                "0 8px 20px rgba(37,99,235,0.3)";
            }}
          >
            Get Started
          </button>
        </div>
      ) : (
        <div
          style={{
            width: "100%",
            maxWidth: "600px",
            height: "80vh",
            maxHeight: "720px",
          }}
        >
          <ChatWindow />
        </div>
      )}
    </div>
  );
}

export default App;
