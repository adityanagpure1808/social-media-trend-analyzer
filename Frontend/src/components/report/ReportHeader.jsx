// export default function ReportHeader({ report }) {
//   return (
//     <div className="bg-white border-b">
//       <div className="max-w-6xl mx-auto px-6 py-8">
//         <h1 className="text-3xl font-bold text-indigo-700">
//           {report.title}
//         </h1>
//         <p className="text-gray-600 mt-2">
//           {report.summary}
//         </p>
//       </div>
//     </div>
//   );
// }



import ReportActions from "./ReportActions";

export default function ReportHeader({ report }) {
  return (
    <div className="bg-white border-b sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-6 py-6 flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-indigo-700">
            {report.title}
          </h1>
          <p className="text-gray-600 mt-1">
            {report.summary}
          </p>
        </div>

        {/* Share / Export actions */}
        <ReportActions report={report} />
      </div>
    </div>
  );
}
