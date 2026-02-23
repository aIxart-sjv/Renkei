import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";

// Context
import { AuthProvider, AuthContext } from "./context/AuthContext";

// Pages
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Recommendations from "./pages/Recommendations";
import Startups from "./pages/Startups";
import Network from "./pages/Network";

// Optional: simple login placeholder (replace later)
const Login = () => {
  return (
    <div style={styles.center}>
      <h2>Renkei Login</h2>
      <p>Login page coming soon</p>
    </div>
  );
};

/**
 * Protected Route Wrapper
 */
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);

  if (loading) {
    return <div style={styles.center}>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

/**
 * Main App Routes
 */
const AppRoutes = () => {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<Login />} />

      {/* Protected */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />

      <Route
        path="/recommendations"
        element={
          <ProtectedRoute>
            <Recommendations />
          </ProtectedRoute>
        }
      />

      <Route
        path="/startups"
        element={
          <ProtectedRoute>
            <Startups />
          </ProtectedRoute>
        }
      />

      <Route
        path="/network"
        element={
          <ProtectedRoute>
            <Network />
          </ProtectedRoute>
        }
      />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

/**
 * Root App Component
 */
export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

/**
 * Simple styles (replace with Tailwind later)
 */
const styles = {
  center: {
    display: "flex",
    height: "100vh",
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "column",
    fontFamily: "Arial, sans-serif",
  },
};