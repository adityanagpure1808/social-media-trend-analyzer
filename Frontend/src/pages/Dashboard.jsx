// import Navbar from "../components/Navbar";
// import PlatformSelector from "../components/PlatformSelector";
// import StatsCards from "../components/StatsCards";
// import RecentReports from "../components/RecentReports";

// export default function Dashboard() {
//   return (
//     <div className="min-h-screen bg-gray-100">
//       <Navbar />

//       <div className="max-w-6xl mx-auto p-6 space-y-10">
//         <StatsCards />
//         <PlatformSelector />
//         <RecentReports />
//       </div>
//     </div>
//   );
// }


// import Navbar from "../components/Navbar";
// import PlatformSelector from "../components/PlatformSelector";
// import StatsCards from "../components/StatsCards";
// import RecentReports from "../components/RecentReports";

// export default function Dashboard() {
//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
//       <Navbar />

//       <div className="max-w-7xl mx-auto px-6 py-10 space-y-12">
//         <StatsCards />
//         <PlatformSelector />
//         <RecentReports />
//       </div>
//     </div>
//   );
// }


// import { useState } from "react";
// import { useAuth } from "../context/AuthContext";

// import Navbar from "../components/Navbar";
// import StatsCards from "../components/StatsCards";
// import PlatformSelector from "../components/PlatformSelector";
// import GenerateReportButton from "../components/GenerateReportButton";
// import ReportStatus from "../components/ReportStatus";
// import RecentReports from "../components/RecentReports";

// export default function Dashboard() {
//   const { user } = useAuth();

//   const [selectedPlatform, setSelectedPlatform] = useState(null);
//   const [reportId, setReportId] = useState(null);

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
//       <Navbar />

//       <div className="max-w-7xl mx-auto px-6 py-10 space-y-12">
//         {/* Top stats */}
//         <StatsCards />

//         {/* Platform selection */}
//         <PlatformSelector onSelect={setSelectedPlatform} />

//         {/* Generate report */}
//         <GenerateReportButton
//           userId={user.uid}
//           platform={selectedPlatform}
//           onReportStarted={setReportId}
//         />

//         {/* Report progress + result */}
//         {reportId && <ReportStatus reportId={reportId} />}

//         {/* History */}
//         <RecentReports />
//       </div>
//     </div>
//   );
// }






// import { useState } from "react";
// import { useAuth } from "../context/AuthContext";

// import Navbar from "../components/Navbar";
// import StatsCards from "../components/StatsCards";
// import PlatformSelector from "../components/PlatformSelector";
// import GenerateReportButton from "../components/GenerateReportButton";
// import ReportStatus from "../components/ReportStatus";
// import RecentReports from "../components/RecentReports";

// export default function Dashboard() {
//   const { user } = useAuth();

//   const [selectedPlatform, setSelectedPlatform] = useState(null);
//   const [reportId, setReportId] = useState(null);

//   // 🔹 REQUIRED for query support
//   const [query, setQuery] = useState("");

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
//       <Navbar />

//       <div className="max-w-7xl mx-auto px-6 py-10 space-y-12">
//         {/* Top stats */}
//         <StatsCards />

//         {/* Platform selection */}
//         <PlatformSelector onSelect={setSelectedPlatform} />

//         {/* Optional query input (minimal, no redesign) */}
//         <input
//           type="text"
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           placeholder="Optional: enter a specific topic or query"
//           className="w-full max-w-xl px-4 py-2 border rounded-lg"
//         />

//         {/* Generate report */}
//         <GenerateReportButton
//           userId={user.uid}
//           platform={selectedPlatform}
//           query={query}
//         />

//         {/* Report progress + result */}
//         {reportId && <ReportStatus reportId={reportId} />}

//         {/* History */}
//         <RecentReports />
//       </div>
//     </div>
//   );
// }





// import { useState } from "react";
// import { useAuth } from "../context/AuthContext";
// import { Link } from "react-router-dom";

// import Navbar from "../components/Navbar";
// import StatsCards from "../components/StatsCards";
// import PlatformSelector from "../components/PlatformSelector";
// import GenerateReportButton from "../components/GenerateReportButton";
// import ReportStatus from "../components/ReportStatus";
// import RecentReports from "../components/RecentReports";

// export default function Dashboard() {
//   const { user } = useAuth();

//   const [selectedPlatform, setSelectedPlatform] = useState(null);
//   const [reportId, setReportId] = useState(null);

//   // 🔹 Query support
//   const [query, setQuery] = useState("");

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
//       <Navbar />

//       <div className="max-w-7xl mx-auto px-6 py-10 space-y-12">
//         {/* Top stats */}
//         <StatsCards />

//         {/* Platform selection */}
//         <PlatformSelector onSelect={setSelectedPlatform} />

//         {/* Optional query input */}
//         <input
//           type="text"
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           placeholder="Optional: enter a specific topic or query"
//           className="w-full max-w-xl px-4 py-2 border rounded-lg"
//         />

//         {/* Generate report */}
//         <GenerateReportButton
//           userId={user.uid}
//           platform={selectedPlatform}
//           query={query}
//         />

//         {/* 🔗 VIEW ALL REPORTS LINK */}
//         <div>
//           <Link
//             to="/reports"
//             className="text-indigo-600 font-medium hover:underline"
//           >
//             View My Reports →
//           </Link>
//         </div>

//         {/* Report progress */}
//         {reportId && <ReportStatus reportId={reportId} />}

//         {/* Recent history */}
//         <RecentReports />
//       </div>
//     </div>
//   );
// }









import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

import Navbar from "../components/Navbar";
import StatsCards from "../components/StatsCards";
import PlatformSelector from "../components/PlatformSelector";
import GenerateReportButton from "../components/GenerateReportButton";
import ReportStatus from "../components/ReportStatus";
import RecentReports from "../components/RecentReports";

import { fetchDashboardStats, fetchUserReports } from "../api";

export default function Dashboard() {
  const { user } = useAuth();

  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [reportId, setReportId] = useState(null);
  const [query, setQuery] = useState("");

  // =========================
  // 🆕 DASHBOARD DATA STATE
  // =========================
  const [stats, setStats] = useState(null);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ⚠️ temp static user until auth fully wired
  const userId = "7GNaHeKgdeXKur24sOCMh6aWy7B2";

  // =========================
  // LOAD DASHBOARD DATA
  // =========================
  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);

        const [statsData, reportsData] = await Promise.all([
          fetchDashboardStats(userId),
          fetchUserReports(userId),
        ]);

        setStats(statsData);
        setReports(reportsData);
      } catch (e) {
        console.error(e);
        setError("Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  // =========================
  // LOADING UI
  // =========================
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading dashboard...</p>
      </div>
    );
  }
  if (loading) return <p className="p-10">Loading dashboard...</p>;
  if (error) return <p className="p-10 text-red-500">{error}</p>;


  // =========================
  // ERROR UI
  // =========================
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  // =========================
  // MAIN UI
  // =========================
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-10 space-y-12">

        {/* 📊 Stats */}
        <StatsCards stats={stats} />

        {/* Platform selection */}
        <PlatformSelector onSelect={setSelectedPlatform} />

        {/* Optional query */}
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Optional: enter a specific topic or query"
          className="w-full max-w-xl px-4 py-2 border rounded-lg"
        />

        {/* Generate report */}
        <GenerateReportButton
          userId={userId}
          platform={selectedPlatform}
          query={query}
          onCreated={(id) => setReportId(id)}
        />

        {/* View all reports */}
        <div>
          <Link
            to="/reports"
            className="text-indigo-600 font-medium hover:underline"
          >
            View My Reports →
          </Link>
        </div>

        {/* Progress */}
        {reportId && <ReportStatus reportId={reportId} />}

        {/* 🧾 Recent Reports */}
        <RecentReports reports={reports} />

      </div>
    </div>
  );
}
