import { useState } from "react";

const API = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function ExportButton({ reportId }) {
  const [loading, setLoading] = useState(false);

  const download = async () => {
    try {
      setLoading(true);

      const res = await fetch(`${API}/api/reports/${reportId}/export`);

      if (!res.ok) throw new Error("Export failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `report_${reportId}.md`;
      document.body.appendChild(a);
      a.click();
      a.remove();

    } catch {
      alert("Failed to export report");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={download}
      disabled={loading}
      className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
    >
      {loading ? "Exporting..." : "Export Report"}
    </button>
  );
}
