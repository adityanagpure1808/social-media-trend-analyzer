


// working

// export default function ChatHistory({ messages, loading }) {
//   return (
//     <div className="flex-1 overflow-y-auto p-4 space-y-3">
//       {messages.map((msg, i) => (
//         <div
//           key={i}
//           className={`max-w-[75%] px-4 py-2 rounded-lg text-sm ${
//             msg.role === "user"
//               ? "ml-auto bg-blue-600 text-white"
//               : "mr-auto bg-gray-100 text-gray-900"
//           }`}
//         >
//           {msg.text}
//         </div>
//       ))}

//       {loading && (
//         <div className="mr-auto bg-gray-100 text-gray-500 px-4 py-2 rounded-lg text-sm">
//           Thinking…
//         </div>
//       )}
//     </div>
//   );
// }





// import MessageBubble from "./MessageBubble";

// export default function ChatHistory({ messages, loading }) {
//   return (
//     <div className="flex-1 overflow-y-auto p-4 space-y-2">
//       {messages.map((m, i) => (
//         <MessageBubble
//           key={i}
//           role={m.role}
//           text={m.text}
//           source={m.source}
//         />
//       ))}

//       {loading && (
//         <div className="text-xs text-gray-400">
//           Assistant is thinking…
//         </div>
//       )}
//     </div>
//   );
// }






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
