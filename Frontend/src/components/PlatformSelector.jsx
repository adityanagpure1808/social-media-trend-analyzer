

// import { useEffect, useState } from "react";
// import { useAuth } from "../context/AuthContext";
// import PlatformCard from "./PlatformCard";

// export default function PlatformSelector({ onSelect }) {
//   const { user } = useAuth();
//   const [selected, setSelected] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [customPlatform, setCustomPlatform] = useState("");

//   const platforms = [
//     {
//       name: "Facebook",
//       value: "facebook",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733547.png"
//           alt="Facebook"
//           width={80}
//         />
//       ),
//     },
//     {
//       name: "LinkedIn",
//       value: "linkedin",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733561.png"
//           alt="LinkedIn"
//           width={80}
//         />
//       ),
//     },
//     {
//       name: "Instagram",
//       value: "instagram",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733558.png"
//           alt="Instagram"
//           width={80}
//         />
//       ),
//     },
//   ];

//   // 🔄 Restore previously selected platform
//   useEffect(() => {
//     if (!user) return;

//     fetch(`http://localhost:8000/api/platform/current/${user.uid}`)
//       .then((res) => res.json())
//       .then((data) => {
//         if (data.platform) {
//           setSelected(data.platform);
//           onSelect?.(data.platform); // ✅ notify parent
//         }
//       });
//   }, [user, onSelect]);

//   const savePlatform = async (platform) => {
//     try {
//       setLoading(true);

//       await fetch("http://localhost:8000/api/platform/select", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           userId: user.uid,
//           platform,
//         }),
//       });

//       setSelected(platform);
//       onSelect?.(platform); // ✅ REQUIRED
//     } catch {
//       alert("Failed to save selection");
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleCustomSubmit = () => {
//     if (!customPlatform.trim()) return;
//     savePlatform(customPlatform.toLowerCase());
//     setCustomPlatform("");
//   };

//   return (
//     <div className="bg-white/70 backdrop-blur-lg p-8 rounded-3xl shadow-xl border border-gray-100">
//       <div className="mb-8 text-center">
//         <h2 className="text-2xl font-bold text-gray-800">
//           Choose Your Platform
//         </h2>
//         <p className="text-gray-500 mt-2 text-sm">
//           Select or enter a social media platform to analyze trends.
//         </p>
//       </div>

//       {/* Predefined platforms */}
//       <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
//         {platforms.map((p) => (
//           <PlatformCard
//             key={p.value}
//             name={p.name}
//             icon={p.icon}
//             selected={selected === p.value}
//             onClick={() => savePlatform(p.value)}
//           />
//         ))}
//       </div>

//       {/* Custom platform input */}
//       <div className="max-w-md mx-auto">
//         <label className="block text-sm font-medium text-gray-700 mb-2">
//           Other Platform
//         </label>

//         <div className="flex gap-2">
//           <input
//             type="text"
//             placeholder="e.g. Reddit, Discord, X, Threads"
//             value={customPlatform}
//             onChange={(e) => setCustomPlatform(e.target.value)}
//             className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
//           />

//           <button
//             onClick={handleCustomSubmit}
//             disabled={loading}
//             className="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
//           >
//             Select
//           </button>
//         </div>
//       </div>

//       {loading && (
//         <p className="text-center mt-6 text-indigo-500 text-sm animate-pulse">
//           Saving selection...
//         </p>
//       )}
//     </div>
//   );
// }






// import { useEffect, useState } from "react";
// import { useAuth } from "../context/AuthContext";
// import PlatformCard from "./PlatformCard";

// export default function PlatformSelector({ onSelect }) {
//   const { user } = useAuth();
//   const [selected, setSelected] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [customPlatform, setCustomPlatform] = useState("");

//   const platforms = [
//     {
//       name: "Facebook",
//       value: "facebook",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733547.png"
//           alt="Facebook"
//           width={80}
//         />
//       ),
//     },
//     {
//       name: "LinkedIn",
//       value: "linkedin",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733561.png"
//           alt="LinkedIn"
//           width={80}
//         />
//       ),
//     },
//     {
//       name: "Instagram",
//       value: "instagram",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733558.png"
//           alt="Instagram"
//           width={80}
//         />
//       ),
//     },
//   ];

//   // 🔹 STEP 3 — NORMALIZE PLATFORM VALUES
//   const normalizePlatform = (value) => {
//     const v = value.toLowerCase();

//     if (v === "x") return "twitter";
//     if (v === "threads") return "instagram";
//     return v;
//   };

//   // Restore previously selected platform
//   useEffect(() => {
//     if (!user) return;

//     fetch(`http://localhost:8000/api/platform/current/${user.uid}`)
//       .then((res) => res.json())
//       .then((data) => {
//         if (data.platform) {
//           setSelected(data.platform);
//           onSelect?.(data.platform);
//         }
//       });
//   }, [user, onSelect]);

//   const savePlatform = async (platform) => {
//     try {
//       setLoading(true);

//       await fetch("http://localhost:8000/api/platform/select", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           userId: user.uid,
//           platform,
//         }),
//       });

//       setSelected(platform);
//       onSelect?.(platform);
//     } catch {
//       alert("Failed to save selection");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // 🔹 STEP 1 + STEP 2 — CUSTOM PLATFORM SELECT
//   const handleCustomSubmit = () => {
//     if (!customPlatform.trim()) return;

//     const normalized = normalizePlatform(customPlatform.trim());

//     setSelected(normalized);
//     onSelect?.(normalized);
//     savePlatform(normalized);

//     setCustomPlatform("");
//   };

//   return (
//     <div className="bg-white/70 backdrop-blur-lg p-8 rounded-3xl shadow-xl border border-gray-100">
//       <div className="mb-8 text-center">
//         <h2 className="text-2xl font-bold text-gray-800">
//           Choose Your Platform
//         </h2>
//         <p className="text-gray-500 mt-2 text-sm">
//           Select or enter a social media platform to analyze trends.
//         </p>
//       </div>

//       {/* Predefined platforms */}
//       <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
//         {platforms.map((p) => (
//           <PlatformCard
//             key={p.value}
//             name={p.name}
//             icon={p.icon}
//             selected={selected === p.value}
//             onClick={() => {
//               setSelected(p.value);
//               onSelect?.(p.value);
//               savePlatform(p.value);
//             }}
//           />
//         ))}
//       </div>

//       {/* Custom platform input */}
//       <div className="max-w-md mx-auto">
//         <label className="block text-sm font-medium text-gray-700 mb-2">
//           Other Platform
//         </label>

//         <div className="flex gap-2">
//           <input
//             type="text"
//             placeholder="e.g. Reddit, Discord, X, Threads"
//             value={customPlatform}
//             onChange={(e) => setCustomPlatform(e.target.value)}
//             className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
//           />

//           {/* 🔑 THIS IS THE KEY FIX */}
//           <button
//             onClick={handleCustomSubmit}
//             disabled={loading}
//             className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
//           >
//             Select
//           </button>
//         </div>
//       </div>

//       {loading && (
//         <p className="text-center mt-6 text-indigo-500 text-sm animate-pulse">
//           Saving selection...
//         </p>
//       )}
//     </div>
//   );
// }






// import { useEffect, useState } from "react";
// import { useAuth } from "../context/AuthContext";
// import PlatformCard from "./PlatformCard";

// const API =
//   import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// export default function PlatformSelector({ onSelect }) {
//   const { user } = useAuth();

//   const [selected, setSelected] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [customPlatform, setCustomPlatform] = useState("");

//   /* ================= PLATFORM LIST ================= */
//   const platforms = [
//     {
//       name: "Facebook",
//       value: "facebook",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733547.png"
//           alt="Facebook"
//           width={80}
//         />
//       ),
//     },
//     {
//       name: "LinkedIn",
//       value: "linkedin",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733561.png"
//           alt="LinkedIn"
//           width={80}
//         />
//       ),
//     },
//     {
//       name: "Instagram",
//       value: "instagram",
//       icon: (
//         <img
//           src="https://cdn-icons-png.flaticon.com/512/733/733558.png"
//           alt="Instagram"
//           width={80}
//         />
//       ),
//     },
//   ];

//   /* ================= NORMALIZE INPUT ================= */
//   const normalizePlatform = (value) => {
//     const v = value.toLowerCase();
//     if (v === "x") return "twitter";
//     if (v === "threads") return "instagram";
//     return v;
//   };

//   /* ================= LOAD CURRENT PLATFORM ================= */
//   useEffect(() => {
//     if (!user?.uid) return;

//     fetch(`${API}/api/platform/current/${user.uid}`)
//       .then((res) => res.json())
//       .then((data) => {
//         if (data?.platform) {
//           setSelected(data.platform);
//           onSelect?.(data.platform);
//         }
//       })
//       .catch(() => {
//         // silent fail — not critical
//       });
//   }, [user?.uid]);

//   /* ================= SAVE PLATFORM ================= */
//   const savePlatform = async (platform) => {
//     if (!user?.uid) return;

//     try {
//       setLoading(true);

//       await fetch(`${API}/api/platform/select`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           userId: user.uid,
//           platform,
//         }),
//       });

//       setSelected(platform);
//       onSelect?.(platform);
//     } catch {
//       alert("Failed to save selection");
//     } finally {
//       setLoading(false);
//     }
//   };

//   /* ================= CUSTOM INPUT ================= */
//   const handleCustomSubmit = () => {
//     if (!customPlatform.trim()) return;

//     const normalized = normalizePlatform(customPlatform.trim());
//     savePlatform(normalized);
//     setCustomPlatform("");
//   };

//   /* ================= UI ================= */
//   return (
//     <div className="bg-white/70 backdrop-blur-lg p-8 rounded-3xl shadow-xl border border-gray-100">
//       <div className="mb-8 text-center">
//         <h2 className="text-2xl font-bold text-gray-800">
//           Choose Your Platform
//         </h2>
//         <p className="text-gray-500 mt-2 text-sm">
//           Select or enter a social media platform to analyze trends.
//         </p>
//       </div>

//       {/* Predefined platforms */}
//       <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
//         {platforms.map((p) => (
//           <PlatformCard
//             key={p.value}
//             name={p.name}
//             icon={p.icon}
//             selected={selected === p.value}
//             onClick={() => savePlatform(p.value)}
//           />
//         ))}
//       </div>

//       {/* Custom platform */}
//       <div className="max-w-md mx-auto">
//         <label className="block text-sm font-medium text-gray-700 mb-2">
//           Other Platform
//         </label>

//         <div className="flex gap-2">
//           <input
//             type="text"
//             placeholder="e.g. Reddit, Discord, X, Threads"
//             value={customPlatform}
//             onChange={(e) => setCustomPlatform(e.target.value)}
//             className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
//           />

//           <button
//             onClick={handleCustomSubmit}
//             disabled={loading}
//             className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
//           >
//             Select
//           </button>
//         </div>
//       </div>

//       {loading && (
//         <p className="text-center mt-6 text-indigo-500 text-sm animate-pulse">
//           Saving selection...
//         </p>
//       )}
//     </div>
//   );
// }









import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import PlatformCard from "./PlatformCard";

const API =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function PlatformSelector({ onSelect }) {
  const { user } = useAuth();

  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [customPlatform, setCustomPlatform] = useState("");

  /* ================= PLATFORM LIST ================= */
  const platforms = [
    {
      name: "Facebook",
      value: "facebook",
      icon: (
        <img
          src="https://cdn-icons-png.flaticon.com/512/733/733547.png"
          alt="Facebook"
          width={80}
        />
      ),
    },
    {
      name: "LinkedIn",
      value: "linkedin",
      icon: (
        <img
          src="https://cdn-icons-png.flaticon.com/512/733/733561.png"
          alt="LinkedIn"
          width={80}
        />
      ),
    },
    {
      name: "Instagram",
      value: "instagram",
      icon: (
        <img
          src="https://cdn-icons-png.flaticon.com/512/733/733558.png"
          alt="Instagram"
          width={80}
        />
      ),
    },
  ];

  /* ================= NORMALIZE INPUT ================= */
  const normalizePlatform = (value) => {
    const v = value.toLowerCase();
    if (v === "x") return "twitter";
    if (v === "threads") return "instagram";
    return v;
  };

  /* ================= LOAD CURRENT PLATFORM ================= */
  useEffect(() => {
    if (!user?.uid) return;

    fetch(`${API}/api/platform/current/${user.uid}`)
      .then((res) => res.json())
      .then((data) => {
        if (data?.platform) {
          setSelected(data.platform);
          onSelect?.(data.platform);
        }
      })
      .catch(() => {
        // silent fail — not critical
      });
  }, [user?.uid]);

  /* ================= SAVE PLATFORM ================= */
  const savePlatform = async (platform) => {
    if (!user?.uid) return;

    try {
      setLoading(true);

      await fetch(`${API}/api/platform/select`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId: user.uid,
          platform,
        }),
      });

      setSelected(platform);
      onSelect?.(platform);
    } catch {
      alert("Failed to save selection");
    } finally {
      setLoading(false);
    }
  };

  /* ================= CUSTOM INPUT ================= */
  const handleCustomSubmit = () => {
    if (!customPlatform.trim()) return;

    const normalized = normalizePlatform(customPlatform.trim());
    savePlatform(normalized);
    setCustomPlatform("");
  };

  /* ================= UI ================= */
  return (
    <div className="bg-white/70 backdrop-blur-lg p-8 rounded-3xl shadow-xl border border-gray-100">
      <div className="mb-8 text-center">
        <h2 className="text-2xl font-bold text-gray-800">
          Choose Your Platform
        </h2>
        <p className="text-gray-500 mt-2 text-sm">
          Select or enter a social media platform to analyze trends.
        </p>
      </div>

      {/* Predefined platforms */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {platforms.map((p) => (
          <PlatformCard
            key={p.value}
            name={p.name}
            icon={p.icon}
            selected={selected === p.value}
            onClick={() => savePlatform(p.value)}
          />
        ))}
      </div>

      {/* Custom platform */}
      <div className="max-w-md mx-auto">
        <label
          htmlFor="customPlatform"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Other Platform
        </label>

        <div className="flex gap-2">
          <input
            id="customPlatform"
            name="customPlatform"
            type="text"
            placeholder="e.g. Reddit, Discord, X, Threads"
            value={customPlatform}
            onChange={(e) => setCustomPlatform(e.target.value)}
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />

          <button
            type="button"
            onClick={handleCustomSubmit}
            disabled={loading}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
          >
            Select
          </button>
        </div>
      </div>

      {loading && (
        <p className="text-center mt-6 text-indigo-500 text-sm animate-pulse">
          Saving selection...
        </p>
      )}
    </div>
  );
}
