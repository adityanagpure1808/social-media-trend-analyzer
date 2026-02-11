export default function PlatformBackground({ text }) {
  if (!text) return null;

  return (
    <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-6 mb-10">
      <h2 className="text-lg font-semibold text-indigo-700 mb-2">
        Platform Trend Background
      </h2>
      <p className="text-gray-700 text-sm leading-relaxed">
        {text}
      </p>
    </div>
  );
}
