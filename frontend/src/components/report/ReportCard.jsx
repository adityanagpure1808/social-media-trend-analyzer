import { useNavigate } from "react-router-dom";

export default function ReportCard({ report }) {
  const navigate = useNavigate();

  return (
    <div
      onClick={() => navigate(`/reports/${report.id}`)}
      className="bg-white p-5 rounded-xl shadow hover:shadow-md cursor-pointer border"
    >
      <div className="flex justify-between">
        <div>
          <h2 className="font-semibold">
            {report.title || "Untitled Report"}
          </h2>
          <p className="text-sm text-gray-500">
            {report.platform} • {new Date(report.created_at).toDateString()}
          </p>
        </div>

        <span className="text-sm capitalize">
          {report.status}
        </span>
      </div>
    </div>
  );
}
