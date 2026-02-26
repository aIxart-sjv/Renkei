import { Link } from "react-router-dom";

function Login() {
  return (
    <div className="page-center">
      <div className="card">
        <h2>Welcome Back</h2>

        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />

        <button>Login</button>

        <p style={{ fontSize: "14px", marginTop: "10px" }}>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;