





const API =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";


/* =========================
   CHAT
========================= */
export async function sendChatMessage(reportId, question) {
  if (!reportId) {
    throw new Error("Missing reportId");
  }

  const res = await fetch(`${API}/api/reports/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: "demo-user",   // ✅ REQUIRED
      report_id: reportId,    // ✅ snake_case
      question: question,     // ✅ required
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Chat request failed");
  }

  return res.json();
}


/* =========================
   CHAT HISTORY
========================= */
export async function fetchChatHistory(reportId) {
  const res = await fetch(`${API}/api/reports/${reportId}/chat`);

  if (!res.ok) {
    throw new Error("Failed to fetch chat history");
  }

  return res.json();
}


/* =========================
   DASHBOARD STATS
========================= */
export async function fetchDashboardStats(userId) {
  const res = await fetch(`${API}/api/dashboard/${userId}`);

  if (!res.ok) {
    throw new Error("Failed to fetch dashboard stats");
  }

  return res.json();
}


/* =========================
   USER REPORTS LIST
========================= */
export async function fetchUserReports(userId) {
  const res = await fetch(`${API}/api/reports/user/${userId}`);

  if (!res.ok) {
    throw new Error("Failed to fetch user reports");
  }

  return res.json();
}
