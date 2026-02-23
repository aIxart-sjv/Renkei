import { NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">

        {/* Logo / Brand */}
        <div className="navbar-logo">
          <NavLink to="/">
            Renkei
          </NavLink>
        </div>

        {/* Navigation Links */}
        <div className="navbar-links">

          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Dashboard
          </NavLink>

          <NavLink
            to="/graph"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Graph
          </NavLink>

          <NavLink
            to="/achievements"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Achievements
          </NavLink>

          <NavLink
            to="/mentors"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Mentors
          </NavLink>

          <NavLink
            to="/startups"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Startups
          </NavLink>

        </div>

      </div>
    </nav>
  );
}

export default Navbar;