// import { useState } from "react";

// export default function LoginForm() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [touched, setTouched] = useState({});

//   const emailValid = /\S+@\S+\.\S+/.test(email);
//   const passwordValid = password.length >= 6;

//   return (
//     <form className="space-y-5">
      
//       {/* Email */}
//       <div>
//         <label className="block text-sm font-semibold text-gray-700 mb-1">
//           Email Address
//         </label>
//         <input
//           type="email"
//           value={email}
//           onBlur={() => setTouched({ ...touched, email: true })}
//           onChange={(e) => setEmail(e.target.value)}
//           className={`w-full px-4 py-2.5 border rounded-lg shadow-sm focus:ring-2 outline-none transition ${
//             touched.email && !emailValid
//               ? "border-red-500 focus:ring-red-200"
//               : "border-gray-300 focus:ring-indigo-200"
//           }`}
//           placeholder="you@example.com"
//         />
//         {touched.email && !emailValid && (
//           <p className="text-red-500 text-xs mt-1">Enter a valid email.</p>
//         )}
//       </div>

//       {/* Password */}
//       <div>
//         <label className="block text-sm font-semibold text-gray-700 mb-1">
//           Password
//         </label>
//         <input
//           type="password"
//           value={password}
//           onBlur={() => setTouched({ ...touched, password: true })}
//           onChange={(e) => setPassword(e.target.value)}
//           className={`w-full px-4 py-2.5 border rounded-lg shadow-sm focus:ring-2 outline-none transition ${
//             touched.password && !passwordValid
//               ? "border-red-500 focus:ring-red-200"
//               : "border-gray-300 focus:ring-indigo-200"
//           }`}
//           placeholder="Enter your password"
//         />
//         {touched.password && !passwordValid && (
//           <p className="text-red-500 text-xs mt-1">
//             Password must be at least 6 characters.
//           </p>
//         )}
//       </div>

//       {/* Button */}
//       <button
//         type="button"
//         className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-2.5 rounded-lg font-semibold shadow-md hover:shadow-lg hover:scale-[1.02] transition transform"
//       >
//         Log In
//       </button>
//     </form>
//   );
// }




import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../config/firebase";
import { useNavigate } from "react-router-dom";

export default function LoginForm() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [touched, setTouched] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const emailValid = /\S+@\S+\.\S+/.test(email);
  const passwordValid = password.length >= 6;

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setTouched({ email: true, password: true });

    if (!emailValid || !passwordValid) return;

    try {
      setLoading(true);
      await signInWithEmailAndPassword(auth, email, password);

      // ✅ Go to dashboard after login
      navigate("/dashboard");
    } catch (err) {
      switch (err.code) {
        case "auth/user-not-found":
          setError("No account found with this email.");
          break;
        case "auth/wrong-password":
          setError("Incorrect password.");
          break;
        case "auth/invalid-email":
          setError("Invalid email format.");
          break;
        default:
          setError("Login failed. Try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleLogin} className="space-y-5">

      {/* Email */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-1">
          Email Address
        </label>
        <input
          type="email"
          value={email}
          onBlur={() => setTouched({ ...touched, email: true })}
          onChange={(e) => setEmail(e.target.value)}
          className={`w-full px-4 py-2.5 border rounded-lg shadow-sm focus:ring-2 outline-none transition ${
            touched.email && !emailValid
              ? "border-red-500 focus:ring-red-200"
              : "border-gray-300 focus:ring-indigo-200"
          }`}
          placeholder="you@example.com"
        />
        {touched.email && !emailValid && (
          <p className="text-red-500 text-xs mt-1">Enter a valid email.</p>
        )}
      </div>

      {/* Password */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-1">
          Password
        </label>
        <input
          type="password"
          value={password}
          onBlur={() => setTouched({ ...touched, password: true })}
          onChange={(e) => setPassword(e.target.value)}
          className={`w-full px-4 py-2.5 border rounded-lg shadow-sm focus:ring-2 outline-none transition ${
            touched.password && !passwordValid
              ? "border-red-500 focus:ring-red-200"
              : "border-gray-300 focus:ring-indigo-200"
          }`}
          placeholder="Minimum 6 characters"
        />
        {touched.password && !passwordValid && (
          <p className="text-red-500 text-xs mt-1">
            Password must be at least 6 characters.
          </p>
        )}
      </div>

      {/* Firebase Error */}
      {error && (
        <p className="text-red-500 text-sm bg-red-50 p-2 rounded-lg">{error}</p>
      )}

      {/* Button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full text-white py-2.5 rounded-lg font-semibold shadow-md transition transform ${
          loading
            ? "bg-indigo-300 cursor-not-allowed"
            : "bg-gradient-to-r from-indigo-600 to-purple-600 hover:shadow-lg hover:scale-[1.02]"
        }`}
      >
        {loading ? "Signing In..." : "Login"}
      </button>
    </form>
  );
}
