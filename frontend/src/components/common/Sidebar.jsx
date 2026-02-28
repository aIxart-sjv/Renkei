// frontend/src/components/common/Sidebar.jsx

import React from "react";
import { NavLink } from "react-router-dom";

const Sidebar = () => {

  const linkClass =
    "block px-4 py-2 rounded-lg transition text-sm font-medium";

  const activeClass =
    "bg-indigo-600 text-white";

  const inactiveClass =
    "text-gray-700 hover:bg-gray-100";

  return (
    <aside className="w-64 h-screen bg-white border-r shadow-sm p-5">

      {/* ========= LOGO ========= */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-indigo-600">
          Renkei
        </h1>
        <p className="text-xs text-gray-500">
          Innovation Intelligence
        </p>
      </div>

      {/* ========= NAVIGATION ========= */}
      <nav className="flex flex-col gap-3">

        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `${linkClass} ${
              isActive ? activeClass : inactiveClass
            }`
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/graph"
          className={({ isActive }) =>
            `${linkClass} ${
              isActive ? activeClass : inactiveClass
            }`
          }
        >
          Graph Intelligence
        </NavLink>

        <NavLink
          to="/students"
          className={({ isActive }) =>
            `${linkClass} ${
              isActive ? activeClass : inactiveClass
            }`
          }
        >
          Students
        </NavLink>

        <NavLink
          to="/mentors"
          className={({ isActive }) =>
            `${linkClass} ${
              isActive ? activeClass : inactiveClass
            }`
          }
        >
          Mentors
        </NavLink>

        <NavLink
          to="/startups"
          className={({ isActive }) =>
            `${linkClass} ${
              isActive ? activeClass : inactiveClass
            }`
          }
        >
          Startups
        </NavLink>

        <NavLink
          to="/recommendations"
          className={({ isActive }) =>
            `${linkClass} ${
              isActive ? activeClass : inactiveClass
            }`
          }
        >
          Recommendations
        </NavLink>

      </nav>

    </aside>
  );
};

export default Sidebar;