import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>🚀 Renkei</h2>

      <div className="nav-links">
        <Link to="/">Dashboard</Link>
        <Link to="/network">Network</Link>
        <Link to="/startups">Startups</Link>
        <Link to="/profile">Profile</Link>
        <Link to="/login">Login</Link>
      </div>
    </nav>
  );
}

export default Navbar;