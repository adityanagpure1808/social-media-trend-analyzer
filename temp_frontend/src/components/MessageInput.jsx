
import { useState } from "react";

export default function MessageInput({ onSend, loading = false }) {
  const [input, setInput] = useState("");

  const send = () => {
    if (!input.trim() || loading) return;

    onSend(input);
    setInput("");
  };

  return (
    <div className="flex gap-2">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask about this report…"
        className="flex-1 border rounded px-3 py-2 text-sm"
        onKeyDown={(e) => e.key === "Enter" && send()}
        disabled={loading}
      />

      <button
        onClick={send}
        disabled={loading}
        className={`px-4 py-2 rounded text-sm ${
          loading
            ? "bg-gray-300 text-gray-600 cursor-not-allowed"
            : "bg-indigo-600 text-white"
        }`}
      >
        {loading ? "Sending…" : "Send"}
      </button>
    </div>
  );
}
