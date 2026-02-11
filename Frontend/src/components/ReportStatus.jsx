



import { useEffect, useRef, useState } from "react";
import ReportView from "./ReportView";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function ReportStatus({ reportId }) {
  const [status, setStatus] = useState("pending");
  const [progress, setProgress] = useState(0);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const intervalRef = useRef(null);
  const abortRef = useRef(null);

  useEffect(() => {
    if (!reportId) return;

    abortRef.current = new AbortController();

    const pollStatus = async () => {
      try {
        const res = await fetch(
          `${API_BASE}/api/reports/${reportId}/status`,
          { signal: abortRef.current.signal }
        );

        if (!res.ok) {
          throw new Error("Failed to fetch report status");
        }

        const data = await res.json();

        if (data.status === "not_found") {
          throw new Error("Report not found");
        }

        setStatus(data.status);
        setProgress(data.progress ?? 0);

        // ✅ stop polling on completion OR failure
        if (data.status === "completed" || data.status === "failed") {
          clearInterval(intervalRef.current);
        }

        if (data.status === "completed") {
          const reportRes = await fetch(
            `${API_BASE}/api/reports/${reportId}`,
            { signal: abortRef.current.signal }
          );

          if (!reportRes.ok) {
            throw new Error("Failed to load report");
          }

          setReport(await reportRes.json());
        }

        if (data.status === "failed") {
          const reportRes = await fetch(
            `${API_BASE}/api/reports/${reportId}`,
            { signal: abortRef.current.signal }
          );

          const failedReport = await reportRes.json();
          setError(
            failedReport.error_message ||
              "Report generation failed"
          );
        }
      } catch (err) {
        if (err.name !== "AbortError") {
          clearInterval(intervalRef.current);
          setError(err.message);
        }
      }
    };

    pollStatus();
    intervalRef.current = setInterval(pollStatus, 3000);

    return () => {
      clearInterval(intervalRef.current);
      abortRef.current?.abort();
    };
  }, [reportId]);

  if (!reportId) return null;

  return (
    <div className="mt-8 bg-white p-6 rounded-xl shadow">
      {!report && !error && (
        <>
          <p className="font-semibold mb-2">
            Status: {status.toUpperCase()}
          </p>

          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </>
      )}

      {error && (
        <p className="text-red-600 font-medium mt-2">
          {error}
        </p>
      )}

      {report && <ReportView report={report} />}
    </div>
  );
}
