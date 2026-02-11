







export default function TopicCard({ topic }) {
  return (
    <span className="inline-block w-full bg-white border rounded-md px-4 py-3 shadow-sm hover:shadow transition">
      <div className="text-sm font-semibold text-gray-800">
        {topic.name || "Unknown Topic"}
      </div>

      <p className="text-xs text-gray-600 mt-1 leading-snug">
        {topic.description || "No description available."}
      </p>

      {/* Source link */}
      {topic.source_url && (
        <a
          href={topic.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="block mt-1 text-xs text-indigo-600 hover:underline"
        >
          🔗 Read source
        </a>
      )}

      {/* 🏷 Hashtags */}
      {topic.hashtags?.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {topic.hashtags.map((tag) => (
            <span
              key={tag}
              className="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/*  Popularity */}
      <div className="mt-2 text-[11px] text-gray-500">
        🔥 Popularity: {topic.popularity ?? "N/A"}
      </div>
    </span>
  );
}
