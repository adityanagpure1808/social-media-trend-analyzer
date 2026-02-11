import { useState } from "react";         

const API_URL = "http://localhost:8000/api/random-quote";
import React from "react";

import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="bg-gray-50 text-gray-800">

      {/* ================= NAVBAR ================= */}
      <nav className="flex justify-between items-center p-6 shadow-md bg-white">
        <h1 className="text-xl font-bold text-blue-600">
          Trend Analyzer
        </h1>

        <div className="space-x-4">
          <Link to="/login" className="text-gray-600 hover:text-blue-600">
            Login
          </Link>
          <Link
            to="/signup"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Sign Up
          </Link>
        </div>
      </nav>


      {/* ================= HERO SECTION ================= */}
      <section className="text-center py-24 px-6 bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <h2 className="text-5xl font-bold mb-6">
          Social Media Trend Analyzer
        </h2>
        <p className="text-lg max-w-2xl mx-auto mb-8">
          Discover trending topics, analyze sentiment, and explore AI-powered
          insights from Facebook, Instagram, and LinkedIn — all in one place.
        </p>
        <Link
          to="/signup"
          className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-200 transition"
        >
          Get Started Free
        </Link>
      </section>


      {/* ================= FEATURES SECTION ================= */}
      <section className="py-20 px-6 max-w-6xl mx-auto">
        <h3 className="text-3xl font-bold text-center mb-12">
          Powerful Features
        </h3>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
            <h4 className="font-semibold text-lg mb-2">AI Trend Reports</h4>
            <p className="text-sm text-gray-600">
              Generate detailed social media trend reports powered by Tavily AI.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
            <h4 className="font-semibold text-lg mb-2">Sentiment Analysis</h4>
            <p className="text-sm text-gray-600">
              Understand how people feel about trending topics and brands.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
            <h4 className="font-semibold text-lg mb-2">Chat with Reports</h4>
            <p className="text-sm text-gray-600">
              Ask questions and explore your reports through an AI chat interface.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
            <h4 className="font-semibold text-lg mb-2">Live Research Fallback</h4>
            <p className="text-sm text-gray-600">
              If your report doesn’t have the answer, AI searches the internet instantly.
            </p>
          </div>
        </div>
      </section>


      {/* ================= HOW IT WORKS SECTION ================= */}
      <section className="bg-white py-20 px-6">
        <h3 className="text-3xl font-bold text-center mb-12">How It Works</h3>

        <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-10 text-center">
          <div>
            <h4 className="font-semibold text-lg mb-2">1. Select Platform</h4>
            <p className="text-gray-600 text-sm">
              Choose Facebook, Instagram, or LinkedIn for analysis.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-lg mb-2">2. Generate Report</h4>
            <p className="text-gray-600 text-sm">
              AI gathers trends and sentiment using Tavily research.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-lg mb-2">3. Ask Questions</h4>
            <p className="text-gray-600 text-sm">
              Use the AI chat to explore insights from your report.
            </p>
          </div>
        </div>
      </section>


      {/* ================= FOOTER ================= */}
      <footer className="text-center py-8 bg-gray-900 text-gray-400">
        <p>© {new Date().getFullYear()} Social Media Trend Analyzer</p>
        <p className="text-sm mt-2">Built with AI-powered trend intelligence</p>
      </footer>

    </div>
  );
}
