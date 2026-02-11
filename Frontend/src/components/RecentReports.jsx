// export default function RecentReports() {
//   const reports = [
//     { id: 1, platform: "Instagram", date: "Jan 25, 2026" },
//     { id: 2, platform: "Facebook", date: "Jan 22, 2026" },
//     { id: 3, platform: "LinkedIn", date: "Jan 18, 2026" },
//   ];

//   return (
//     <div>
//       <h2 className="text-xl font-semibold mb-4">Recent Reports</h2>

//       <div className="bg-white rounded-xl shadow divide-y">
//         {reports.map((r) => (
//           <div key={r.id} className="p-4 flex justify-between">
//             <span>{r.platform}</span>
//             <span className="text-gray-500 text-sm">{r.date}</span>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }


// export default function RecentReports() {
//   const reports = [
//     { id: 1, platform: "Instagram", date: "Jan 25, 2026" },
//     { id: 2, platform: "Facebook", date: "Jan 22, 2026" },
//     { id: 3, platform: "LinkedIn", date: "Jan 18, 2026" },
//   ];

//   return (
//     <div>
//       <h2 className="text-2xl font-bold mb-6">Recent Reports</h2>

//       <div className="bg-white rounded-2xl shadow-md overflow-hidden">
//         {reports.map((r) => (
//           <div
//             key={r.id}
//             className="flex justify-between items-center px-6 py-4 border-b last:border-none hover:bg-indigo-50 transition"
//           >
//             <span className="font-medium">{r.platform}</span>
//             <span className="text-sm text-gray-500">{r.date}</span>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }





export default function RecentReports({ reports }) {
  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="font-semibold mb-3">Recent Reports</h2>

      {reports.map(r => (
        <div key={r.id} className="border-b py-2">
          <p className="font-medium">{r.platform}</p>
          <p className="text-sm text-gray-500">{r.status}</p>
        </div>
      ))}
    </div>
  );
}
