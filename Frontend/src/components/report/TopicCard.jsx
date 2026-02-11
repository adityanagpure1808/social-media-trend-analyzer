


// export default function TopicCard({ topic }) {
//   const hashtags = Array.isArray(topic.hashtags)
//     ? topic.hashtags
//     : [];

//   return (
//     <div className="bg-white rounded-xl shadow p-6 border hover:shadow-md transition">
//       <h2 className="text-lg font-semibold mb-2">
//         {topic.name || "Unknown Topic"}
//       </h2>

//       <p className="text-gray-600 text-sm mb-4">
//         {topic.description || "No description available."}
//       </p>

//       {hashtags.length > 0 && (
//         <div className="flex flex-wrap gap-2 mb-4">
//           {hashtags.map((tag, i) => (
//             <span
//               key={i}
//               className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded"
//             >
//               {tag}
//             </span>
//           ))}
//         </div>
//       )}

//       <p className="text-sm font-medium">
//         Popularity:{" "}
//         <span className="text-indigo-600">
//           {topic.popularity ?? "N/A"}
//         </span>
//       </p>
//     </div>
//   );
// }



export default function TopicCard({ topic }) {
  const hashtags = Array.isArray(topic?.hashtags)
    ? topic.hashtags
    : [];

  return (
    <div className="bg-white rounded-xl shadow p-6 border hover:shadow-md transition flex flex-col">
      <h2 className="text-lg font-semibold mb-2">
        {topic?.name || "Unknown Topic"}
      </h2>

      <p className="text-gray-600 text-sm mb-4">
        {topic?.description || "No description available."}
      </p>

      {hashtags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {hashtags.map((tag, i) => (
            <span
              key={i}
              className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      <div className="mt-auto flex justify-between items-center">
        <span className="text-sm font-medium">
          Popularity:{" "}
          <span className="text-indigo-600">
            {topic?.popularity ?? "N/A"}
          </span>
        </span>

        {topic?.source_url && (
          <a
            href={topic.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-indigo-600 hover:underline"
          >
            View Source ↗
          </a>
        )}
      </div>
    </div>
  );
}
