export default function ReportActions({ report }) {
  const shareUrl = window.location.href;

  const copyLink = async () => {
    await navigator.clipboard.writeText(shareUrl);
    alert("Report link copied!");
  };

  const downloadJSON = () => {
    const blob = new Blob(
      [JSON.stringify(report, null, 2)],
      { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${report.title}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadText = () => {
    const text = `
${report.title}

Summary:
${report.summary}

Trending Topics:
${report.trending_topics.map(
  (t) =>
    `- ${t.name}
  Description: ${t.description}
  Hashtags: ${t.hashtags.join(", ")}
  Popularity: ${t.popularity}`
).join("\n\n")}
`;

    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${report.title}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex gap-3">
      <button
        onClick={copyLink}
        className="px-3 py-1 text-sm border rounded hover:bg-gray-100"
      >
        Copy Link
      </button>

      <button
        onClick={downloadText}
        className="px-3 py-1 text-sm border rounded hover:bg-gray-100"
      >
        Export TXT
      </button>

      <button
        onClick={downloadJSON}
        className="px-3 py-1 text-sm border rounded hover:bg-gray-100"
      >
        Export JSON
      </button>
    </div>
  );
}
