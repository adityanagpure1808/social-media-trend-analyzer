export default function ReportView({ report }) {
  return (
    <div className="mt-8 space-y-6">
      <h1 className="text-2xl font-bold text-indigo-700">
        {report.title}
      </h1>

      <p className="text-gray-600">{report.summary}</p>

      <section>
        <h2 className="font-semibold mb-2">Trending Topics</h2>
        <ul className="space-y-1">
          {report.trending_topics.map((t, i) => (
            <li key={i} className="flex justify-between">
              <span>• {t.topic}</span>
              <span className="text-indigo-600 font-medium">
                {t.growth}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="font-semibold mb-2">Sentiment Analysis</h2>
        <p className="mb-1">
          Overall:{" "}
          <span className="font-bold capitalize">
            {report.sentiment_analysis.overall}
          </span>
        </p>
        <p>Positive: {report.sentiment_analysis.positive}%</p>
        <p>Neutral: {report.sentiment_analysis.neutral}%</p>
        <p>Negative: {report.sentiment_analysis.negative}%</p>
      </section>
    </div>
  );
}
