// frontend/src/components/common/Navbar.jsx

import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = ({ user, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    if (onLogout) onLogout();
    navigate("/login");
  };

  return (
    <nav className="w-full bg-white shadow-md px-6 py-4 flex justify-between items-center">
      
      {/* ================= LOGO ================= */}
      <Link
        to="/dashboard"
        className="text-xl font-bold text-indigo-600"
      >
        Renkei
      </Link>

      {/* ================= NAV LINKS ================= */}
      <div className="flex items-center gap-6">

        <Link
          to="/dashboard"
          className="text-gray-700 hover:text-indigo-600 transition"
        >
          Dashboard
        </Link>

        <Link
          to="/graph"
          className="text-gray-700 hover:text-indigo-600 transition"
        >
          Graph
        </Link>

        <Link
          to="/students"
          className="text-gray-700 hover:text-indigo-600 transition"
        >
          Students
        </Link>

        <Link
          to="/startups"
          className="text-gray-700 hover:text-indigo-600 transition"
        >
          Startups
        </Link>

        <Link
          to="/mentors"
          className="text-gray-700 hover:text-indigo-600 transition"
        >
          Mentors
        </Link>

        {/* ================= USER ================= */}
        {user && (
          <div className="flex items-center gap-4 ml-4">
            <span className="text-sm text-gray-600">
              {user.full_name}
            </span>

            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-3 py-1 rounded-lg hover:bg-red-600 transition"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;