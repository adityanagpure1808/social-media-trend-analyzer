


import TopicCard from "./TopicCard";

export default function TopicGrid({ topics = [] }) {
  if (!topics.length) {
    return (
      <p className="text-center text-gray-500">
        No trending topics available.
      </p>
    );
  }

  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {topics.map((topic, index) => (
        <TopicCard key={index} topic={topic} />
      ))}
    </div>
  );
}
