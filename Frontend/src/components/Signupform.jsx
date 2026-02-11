// import { useState } from "react";

// export default function SignupForm() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [touched, setTouched] = useState({});

//   const emailValid = /\S+@\S+\.\S+/.test(email);
//   const passwordValid = password.length >= 6;

//   return (
//     <form className="bg-white shadow-lg rounded-xl p-8 space-y-6">
      
//       {/* Email Field */}
//       <div>
//         <label className="block text-sm font-medium text-gray-700 mb-1">
//           Email Address
//         </label>
//         <input
//           type="email"
//           value={email}
//           onBlur={() => setTouched({ ...touched, email: true })}
//           onChange={(e) => setEmail(e.target.value)}
//           className={`w-full px-4 py-2 border rounded-lg focus:ring-2 outline-none ${
//             touched.email && !emailValid
//               ? "border-red-500 focus:ring-red-200"
//               : "border-gray-300 focus:ring-indigo-200"
//           }`}
//           placeholder="you@example.com"
//         />
//         {touched.email && !emailValid && (
//           <p className="text-red-500 text-sm mt-1">Enter a valid email.</p>
//         )}
//       </div>

//       {/* Password Field */}
//       <div>
//         <label className="block text-sm font-medium text-gray-700 mb-1">
//           Password
//         </label>
//         <input
//           type="password"
//           value={password}
//           onBlur={() => setTouched({ ...touched, password: true })}
//           onChange={(e) => setPassword(e.target.value)}
//           className={`w-full px-4 py-2 border rounded-lg focus:ring-2 outline-none ${
//             touched.password && !passwordValid
//               ? "border-red-500 focus:ring-red-200"
//               : "border-gray-300 focus:ring-indigo-200"
//           }`}
//           placeholder="Minimum 6 characters"
//         />
//         {touched.password && !passwordValid && (
//           <p className="text-red-500 text-sm mt-1">
//             Password must be at least 6 characters.
//           </p>
//         )}
//       </div>

//       {/* Submit Button (visual only) */}
//       <button
//         type="button"
//         className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition"
//       >
//         Sign Up
//       </button>
//     </form>
//   );
// }





import { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../config/firebase";
import { useNavigate } from "react-router-dom";

export default function SignupForm() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [touched, setTouched] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const emailValid = /\S+@\S+\.\S+/.test(email);
  const passwordValid = password.length >= 6;

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    // Trigger validation display
    setTouched({ email: true, password: true });

    if (!emailValid || !passwordValid) return;

    try {
      setLoading(true);

      await createUserWithEmailAndPassword(auth, email, password);

      // Redirect after success
      navigate("/login");
    } catch (err) {
      switch (err.code) {
        case "auth/email-already-in-use":
          setError("This email is already registered.");
          break;
        case "auth/invalid-email":
          setError("Invalid email address.");
          break;
        case "auth/weak-password":
          setError("Password is too weak.");
          break;
        default:
          setError("Something went wrong. Try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSignup} className="space-y-5">
      
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
        {loading ? "Creating Account..." : "Create Account"}
      </button>
    </form>
  );
}
