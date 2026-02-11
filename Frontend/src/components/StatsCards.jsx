



import { BarChart3, CheckCircle2, AlertTriangle } from "lucide-react";

/* ================= CARD ================= */
function Card({ title, value, icon, color, trend }) {
  return (
    <div
      className="
      bg-white 
      p-6 
      rounded-2xl 
      border border-gray-200
      shadow-sm
      hover:shadow-lg 
      hover:-translate-y-0.5
      transition-all duration-200 ease-out
    "
    >
      <div className={`mb-3 ${color}`}>{icon}</div>

      <p className="text-gray-500 text-sm">{title}</p>

      <p className="text-3xl font-semibold mt-1 text-gray-900">
        {value ?? 0}
      </p>

      {trend && (
        <p className="text-xs text-gray-400 mt-2">
          {trend}
        </p>
      )}
    </div>
  );
}

/* ================= SKELETON ================= */
function Skeleton() {
  return (
    <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 animate-pulse">
      <div className="h-28 bg-gray-200 rounded-2xl"></div>
      <div className="h-28 bg-gray-200 rounded-2xl"></div>
      <div className="h-28 bg-gray-200 rounded-2xl"></div>
    </div>
  );
}

/* ================= MAIN COMPONENT ================= */
export default function StatsCards({ stats }) {
  if (!stats) return <Skeleton />;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6 text-gray-900">
        Overview
      </h2>

      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6">

        <Card
          title="Total Reports"
          value={stats.total_reports}
          icon={<BarChart3 size={30} />}
          color="text-indigo-600"
          trend="Across all platforms"
        />

        <Card
          title="Completed Reports"
          value={stats.completed_reports}
          icon={<CheckCircle2 size={30} />}
          color="text-emerald-600"
          trend="Successfully generated"
        />

        <Card
          title="Failed Reports"
          value={stats.failed_reports}
          icon={<AlertTriangle size={30} />}
          color="text-red-500"
          trend="Needs attention"
        />

      </div>
    </div>
  );
}
