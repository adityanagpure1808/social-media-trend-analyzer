

import { Link } from "react-router-dom";
import SignupForm from "../components/SignupForm.jsx";

export default function Signup() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 via-white to-purple-100 px-4 relative overflow-hidden">
      
      {/* Background blur blobs */}
      <div className="absolute w-72 h-72 bg-indigo-300 rounded-full blur-3xl opacity-20 -top-10 -left-10"></div>
      <div className="absolute w-72 h-72 bg-purple-300 rounded-full blur-3xl opacity-20 bottom-0 right-0"></div>

      <div className="relative w-full max-w-md">
        
        {/* Glass Card */}
        <div className="backdrop-blur-lg bg-white/80 shadow-2xl rounded-2xl p-8 border border-white/40">
          
          <h1 className="text-3xl font-extrabold text-center text-indigo-600 mb-2">
            Join TrendAnalyzer 
          </h1>
          <p className="text-center text-gray-500 text-sm mb-6">
            Start exploring social media trends with AI-powered insights
          </p>

          <SignupForm />

          <p className="text-center text-sm text-gray-600 mt-6">
            Already have an account?{" "}
            <Link to="/" className="text-indigo-600 font-medium hover:underline">
              Back to Home
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
