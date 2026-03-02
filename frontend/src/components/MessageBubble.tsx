import React from "react";

type Role = "user" | "assistant";

interface MessageBubbleProps {
  role: Role;
  content: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ role, content }) => {
  const isUser = role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        width: "100%",
        marginBottom: "8px",
      }}
    >
      <div
        style={{
          maxWidth: "70%",
          padding: "8px 12px",
          borderRadius: "16px",
          fontSize: "14px",
          lineHeight: 1.4,
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          backgroundColor: isUser ? "#007bff" : "#e5e5ea",
          color: isUser ? "#ffffff" : "#000000",
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
        }}
      >
        {content}
      </div>
    </div>
  );
};

