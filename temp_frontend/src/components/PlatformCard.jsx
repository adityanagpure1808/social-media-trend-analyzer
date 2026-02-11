

export default function PlatformCard({ name, icon, selected, onClick }) {
  return (
    <div
      onClick={onClick}
      className={`group p-6 rounded-2xl cursor-pointer transition-all duration-300 border-2 flex flex-col items-center text-center
        ${
          selected
            ? "border-indigo-600 bg-gradient-to-br from-indigo-50 to-purple-50 shadow-lg scale-[1.03]"
            : "border-gray-200 bg-white hover:shadow-2xl hover:-translate-y-1 hover:border-indigo-400"
        }`}
    >
      <div
        className={`mb-4 transition-transform duration-300
          ${selected ? "scale-110 text-indigo-600" : "group-hover:scale-110 text-gray-600 group-hover:text-indigo-600"}`}
      >
        {icon}
      </div>

      <h3
        className={`text-lg font-semibold transition-colors
          ${selected ? "text-indigo-600" : "text-gray-700 group-hover:text-indigo-600"}`}
      >
        {name}
      </h3>

      {selected && (
        <p className="text-xs mt-2 text-indigo-500 font-medium">
          ✓ Selected
        </p>
      )}
    </div>
  );
}
