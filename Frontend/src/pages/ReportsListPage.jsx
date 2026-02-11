import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

const API = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function ReportsListPage() {
  const { user } = useAuth();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    fetch(`${API}/api/reports/user/${user.uid}`)
      .then((res) => res.json())
      .then((data) => {
        setReports(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [user]);

  if (loading) {
    return <p className="p-6">Loading reports...</p>;
  }

  if (!reports.length) {
    return (
      <div className="p-6">
        <p className="text-gray-600">No reports found.</p>
        <Link
          to="/dashboard"
          className="text-indigo-600 font-medium mt-4 inline-block"
        >
          ← Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 space-y-6">
      <h1 className="text-2xl font-bold">My Reports</h1>

      <div className="grid gap-4">
        {reports.map((report) => (
          <Link
            key={report.id}
            to={`/reports/${report.id}`}
            className="p-4 border rounded-lg hover:bg-gray-50 transition"
          >
            <p className="font-semibold capitalize">
              {report.platform} Report
            </p>
            <p className="text-sm text-gray-500">
              {new Date(report.created_at).toLocaleString()}
            </p>
            <p className="text-sm mt-1">
              Status:{" "}
              <span className="font-medium">{report.status}</span>
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
