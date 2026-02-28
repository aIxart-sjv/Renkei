import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import "./App.css"

// Pages
import Login from "./pages/Login"
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard"
import Students from "./pages/Students"
import Mentors from "./pages/Mentors"
import Startups from "./pages/Startups"
import Graph from "./pages/Graph"
import Recommendations from "./pages/Recommendations"

// Layout components (we'll create later)
import Navbar from "./components/common/Navbar"
import Sidebar from "./components/common/Sidebar"

// Simple layout wrapper
function Layout({ children }) {
  return (
    <div className="app-container">

      <Sidebar />

      <div className="main-section">

        <Navbar />

        <div className="content">
          {children}
        </div>

      </div>

    </div>
  )
}

// Protected route
function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token")

  if (!token) {
    return <Navigate to="/" replace />
  }

  return children
}

function App() {
  return (
    <BrowserRouter>

      <Routes>

        {/* Public route */}
        <Route path="/" element={<Login />} />

        {/* Protected routes */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/students"
          element={
            <ProtectedRoute>
              <Layout>
                <Students />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/mentors"
          element={
            <ProtectedRoute>
              <Layout>
                <Mentors />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/startups"
          element={
            <ProtectedRoute>
              <Layout>
                <Startups />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/graph"
          element={
            <ProtectedRoute>
              <Layout>
                <Graph />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/recommendations"
          element={
            <ProtectedRoute>
              <Layout>
                <Recommendations />
              </Layout>
            </ProtectedRoute>
          }
        />

      </Routes>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App