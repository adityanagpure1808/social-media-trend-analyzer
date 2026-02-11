
import { signOut } from "firebase/auth";
import { auth } from "../config/firebase";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await signOut(auth);
    navigate("/login");
  };

  return (
    <nav className="backdrop-blur bg-white/70 sticky top-0 z-50 border-b">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Social Trend Analyzer
        </h1>

        <button
          onClick={handleLogout}
          className="px-4 py-2 rounded-lg bg-red-500 text-white font-medium hover:bg-red-600 hover:scale-105 transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}

