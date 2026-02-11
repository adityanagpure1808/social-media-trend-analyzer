




import { useParams } from "react-router-dom";
import { useEffect, useRef, useState } from "react";

import ReportHeader from "../components/report/ReportHeader";
import PlatformBackground from "../components/report/PlatformBackground";
import TopicGrid from "../components/report/TopicGrid";
import ChatDrawer from "../components/ChatDrawer";
import ExportButton from "../components/ExportButton"; // ✅ EXPORT BUTTON

const API =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function ReportPage() {
  const { reportId } = useParams();

  const [status, setStatus] = useState("pending");
  const [progress, setProgress] = useState(0);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const intervalRef = useRef(null);

  useEffect(() => {
    if (!reportId) return;

    const pollStatus = async () => {
      try {
        const res = await fetch(`${API}/api/reports/${reportId}/status`);

        if (!res.ok) {
          throw new Error("Failed to fetch report status");
        }

        const data = await res.json();

        setStatus(data.status);
        setProgress(data.progress ?? 0);

        // ✅ Completed → fetch final report
        if (data.status === "completed") {
          clearInterval(intervalRef.current);

          const reportRes = await fetch(`${API}/api/reports/${reportId}`);

          if (!reportRes.ok) {
            throw new Error("Failed to load report");
          }

          setReport(await reportRes.json());
        }

        // ❌ Failed
        if (data.status === "failed") {
          clearInterval(intervalRef.current);
          setError("Report generation failed");
        }
      } catch (err) {
        clearInterval(intervalRef.current);
        setError(err.message);
      }
    };

    // Run immediately
    pollStatus();

    // Poll every 3 seconds
    intervalRef.current = setInterval(pollStatus, 3000);

    return () => clearInterval(intervalRef.current);
  }, [reportId]);

  /* ================= LOADING STATE ================= */
  if (!report && !error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <p className="font-semibold mb-3">Generating report…</p>

        <div className="w-64 bg-gray-200 h-2 rounded">
          <div
            className="bg-indigo-600 h-2 rounded transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>

        <p className="text-sm text-gray-500 mt-2">Status: {status}</p>
      </div>
    );
  }

  /* ================= ERROR STATE ================= */
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-600 font-medium">{error}</p>
      </div>
    );
  }

  /* ================= FINAL REPORT ================= */
  return (
    <div className="min-h-screen bg-slate-50">

      {/* Header + Export Button */}
      <div className="max-w-6xl mx-auto px-6 pt-6">
        <div className="flex items-center justify-between gap-4">
          <ReportHeader report={report} />
          <ExportButton reportId={reportId} />
        </div>
      </div>

      {/* Platform Background */}
      {report.platform_background && (
        <PlatformBackground text={report.platform_background} />
      )}

      {/* Topics */}
      <div className="max-w-6xl mx-auto px-6 py-10">
        <TopicGrid topics={report.trending_topics} />
      </div>

      {/* Chat Section */}
      <div className="max-w-6xl mx-auto px-6 pb-16">
        <div className="h-[500px] bg-white rounded-lg shadow">
          <ChatDrawer reportId={reportId} />
        </div>
      </div>

    </div>
  );
}
