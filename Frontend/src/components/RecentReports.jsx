// export default function RecentReports() {





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
