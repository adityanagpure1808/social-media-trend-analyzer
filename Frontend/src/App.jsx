

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Landing from "./pages/Landing";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ReportsListPage from "./pages/ReportsListPage";
import ReportPage from "./pages/ReportPage";

import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    // <BrowserRouter>
      <Routes>
        {/* ================= PUBLIC ROUTES ================= */}
        <Route path="/" element={<Landing />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />

        {/* ================= PROTECTED ROUTES ================= */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* 📄 Reports list */}
        <Route
          path="/reports"
          element={
            <ProtectedRoute>
              <ReportsListPage />
            </ProtectedRoute>
          }
        />

        {/* 📊 Single report detail (ONLY PLACE) */}
        <Route
          path="/reports/:reportId"
          element={
            <ProtectedRoute>
              <ReportPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    //  </BrowserRouter> 
  );
}
