// frontend/src/pages/Dashboard.jsx

import { useEffect, useState } from "react";
import "./Dashboard.css";

import Navbar from "../components/common/Navbar";
import Sidebar from "../components/common/Sidebar";
import GraphView from "../components/graph/GraphView";

import useAuth from "../hooks/useAuth";
import { getGraphData } from "../api/graph";

const Dashboard = () => {

  const { user } = useAuth();

  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await getGraphData();
      setGraphData(data);
    } catch (err) {
      console.error("Dashboard load failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-layout">

      <Sidebar />

      <div className="dashboard-main">

        <Navbar />

        <div className="dashboard-content">

          {/* HEADER */}
          <div className="dashboard-header">
            <h1>Innovation Network</h1>
            <p>
              Welcome back, <strong>{user?.username}</strong>
            </p>
          </div>

          {/* STATS */}
          <div className="dashboard-stats">

            <div className="stat-card">
              <h3>Students</h3>
              <span>{graphData?.nodes?.filter(n => n.type === "student").length || 0}</span>
            </div>

            <div className="stat-card">
              <h3>Mentors</h3>
              <span>{graphData?.nodes?.filter(n => n.type === "mentor").length || 0}</span>
            </div>

            <div className="stat-card">
              <h3>Startups</h3>
              <span>{graphData?.nodes?.filter(n => n.type === "startup").length || 0}</span>
            </div>

            <div className="stat-card">
              <h3>Connections</h3>
              <span>{graphData?.edges?.length || 0}</span>
            </div>

          </div>

          {/* GRAPH */}
          <div className="dashboard-graph">

            {loading ? (
              <p>Loading innovation graph...</p>
            ) : (
              <GraphView data={graphData} />
            )}

          </div>

        </div>

      </div>

    </div>
  );
};

export default Dashboard;