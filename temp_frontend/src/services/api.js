

const API =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * Send a chat message about a report
 */
export async function sendChatMessage(reportId, question) {
  const res = await fetch(`${API}/api/reports/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: "demo-user",   
      report_id: reportId,
      question: question,
    }),
  });

  if (!res.ok) {
    throw new Error("Chat failed");
  }

  return res.json();
}

/**
 * Fetch chat history for a report
 */
export async function fetchChatHistory(reportId) {
  const res = await fetch(
    `${API}/api/reports/${reportId}/chat`
  );

  if (!res.ok) {
    throw new Error("History failed");
  }

  return res.json();
}  


