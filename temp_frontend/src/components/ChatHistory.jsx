





import MessageBubble from "./MessageBubble";

export default function ChatHistory({ messages = [], loading = false }) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-2">
      {messages.map((m, i) => (
        <MessageBubble
          key={i}
          role={m.role}
          text={m.text}
          source={m.source}
        />
      ))}

      {loading && (
        <div className="text-xs text-gray-400">
          Assistant is thinking…
        </div>
      )}
    </div>
  );
}
