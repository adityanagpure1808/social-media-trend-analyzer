






import { useEffect, useState, useRef } from "react";
import ChatHistory from "./ChatHistory";
import MessageInput from "./MessageInput";
import { fetchChatHistory, sendChatMessage } from "../api";

export default function ChatInterface({ reportId }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi 👋 How can I help you with this report?",
      source: "system",
    },
  ]);

  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  // =========================
  // LOAD CHAT HISTORY
  // =========================
  useEffect(() => {
    if (!reportId) return;

    fetchChatHistory(reportId)
      .then((history = []) => {
        if (!history.length) return;

        const formatted = history.flatMap((m) => [
          { role: "user", text: m.question },
          { role: "assistant", text: m.answer, source: m.source },
        ]);

        setMessages((prev) => [...prev, ...formatted]);
      })
      .catch(() => {
        // history is optional
      });
  }, [reportId]);

  // =========================
  // AUTO SCROLL
  // =========================
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // =========================
  // SEND MESSAGE (FIXED)
  // =========================
  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // 1️⃣ Show user message immediately
    setMessages((prev) => [...prev, { role: "user", text }]);
    setLoading(true);

    try {
      const res = await sendChatMessage(reportId, text);

      // 2️⃣ Add assistant reply WITH SOURCE
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: res.answer,
          source: res.source, // rag | tavily
        },
      ]);
    } catch {
      // 3️⃣ Graceful fallback
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Sorry, something went wrong.",
          source: "error",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full border rounded-lg overflow-hidden bg-white">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <ChatHistory messages={messages} loading={loading} />
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t p-3">
        <MessageInput onSend={sendMessage} loading={loading} />
      </div>
    </div>
  );
}
