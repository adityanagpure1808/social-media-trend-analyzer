import { Link } from "react-router-dom";
import LoginForm from "../components/Loginform";

export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 via-white to-purple-100 px-4 relative overflow-hidden">
      
      {/* Background glow blobs */}
      <div className="absolute w-72 h-72 bg-indigo-300 rounded-full blur-3xl opacity-20 -top-10 -left-10"></div>
      <div className="absolute w-72 h-72 bg-purple-300 rounded-full blur-3xl opacity-20 bottom-0 right-0"></div>

      <div className="relative w-full max-w-md">
        <div className="backdrop-blur-lg bg-white/80 shadow-2xl rounded-2xl p-8 border border-white/40">
          
          <h1 className="text-3xl font-extrabold text-center text-indigo-600 mb-2">
            Welcome Back 
          </h1>
          <p className="text-center text-gray-500 text-sm mb-6">
            Log in to explore real-time social media trends
          </p>

          <LoginForm />

          <p className="text-center text-sm text-gray-600 mt-6">
            Don’t have an account?{" "}
            <Link to="/signup" className="text-indigo-600 font-medium hover:underline">
              Sign up
            </Link>
          </p>

          <p className="text-center text-sm mt-2">
            <Link to="/" className="text-gray-500 hover:underline">
              ← Back to Home
            </Link>
          </p>

        </div>
      </div>
    </div>
  );
}
