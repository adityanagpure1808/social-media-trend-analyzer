// import { useState } from "react";

// export default function MessageInput({ onSend, disabled }) {
//   const [text, setText] = useState("");

//   const send = () => {
//     if (!text.trim()) return;
//     onSend(text);
//     setText("");
//   };

//   return (
//     <div className="flex p-3 border-t">
//       <input
//         value={text}
//         onChange={(e) => setText(e.target.value)}
//         disabled={disabled}
//         className="flex-1 border rounded px-3 py-2"
//         placeholder="Ask about this report..."
//       />
//       <button
//         onClick={send}
//         disabled={disabled}
//         className="ml-2 bg-blue-600 text-white px-4 py-2 rounded"
//       >
//         Send
//       </button>
//     </div>
//   );
// }
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
