





export default function MessageBubble({ role, text, source }) {
  const isAssistant = role === "assistant";

  return (
    <div className={`flex ${isAssistant ? "justify-start" : "justify-end"} mb-2`}>
      <div
        className={`max-w-[75%] rounded-lg px-4 py-2 text-sm ${
          isAssistant ? "bg-gray-100 text-gray-900" : "bg-indigo-600 text-white"
        }`}
      >
        <p>{text}</p>

        {/* SOURCE BADGE */}
        {isAssistant && source && source !== "system" && (
          <p className="text-xs text-gray-500 mt-1">
            Source: {source === "report" ? "Report" : "Web (Tavily)"}
          </p>
        )}
      </div>
    </div>
  );
}
