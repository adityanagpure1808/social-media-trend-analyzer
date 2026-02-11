import { useState } from "react";
import ChatInterface from "./ChatInterface";

export default function ChatDrawer({ reportId }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Collapsed Bar */}
      {!open && (
        <div
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 cursor-pointer bg-blue-600 text-white px-5 py-3 rounded-full shadow-lg hover:bg-blue-700 transition"
        >
          💬 Ask about this report
        </div>
      )}

      {/* Drawer */}
      {open && (
        <div className="fixed bottom-0 right-0 w-full sm:w-[420px] h-[520px] bg-white border rounded-t-xl shadow-2xl flex flex-col animate-slideUp">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b bg-gray-50 rounded-t-xl">
            <div className="font-semibold text-gray-800">
               Assistant
            </div>
            <button
              onClick={() => setOpen(false)}
              className="text-gray-500 hover:text-gray-800 text-lg"
            >
              ✕
            </button>
          </div>

          {/* Chat Body */}
          <ChatInterface reportId={reportId} />
        </div>
      )}
    </>
  );
}
