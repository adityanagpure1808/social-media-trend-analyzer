


import { useNavigate } from "react-router-dom";
import { useState } from "react";

const API =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function GenerateReportButton({
  userId,
  platform,
  query,
}) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generate = async () => {
    if (!platform) {
      alert("Please select a platform first");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const res = await fetch(`${API}/api/report/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId,
          platform,
          query,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to start report generation");
      }

      const data = await res.json();

      if (!data?.report_id) {
        throw new Error("Invalid response from server");
      }

      // ✅ Redirect to report page
      navigate(`/reports/${data.report_id}`);
    } catch (err) {
      console.error(err); // keep for debugging
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <button
        onClick={generate}
        disabled={loading}
        className={`px-6 py-2 rounded-lg font-semibold text-white transition
          ${
            loading
              ? "bg-indigo-400 cursor-not-allowed"
              : "bg-indigo-600 hover:bg-indigo-700"
          }`}
      >
        {loading ? "Generating…" : "Generate Report"}
      </button>

      {error && (
        <p className="text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
