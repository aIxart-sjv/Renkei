import { useEffect, useState } from "react";
import GraphView from "../components/GraphView";
import api from "../services/api";
import "../App.css";

export default function Network() {
  const [graphData, setGraphData] = useState({
    nodes: [],
    edges: [],
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGraph();
  }, []);

  const fetchGraph = async () => {
    try {
      setLoading(true);

      // Backend endpoint: GET /graph
      const response = await api.get("/graph");

      setGraphData(response.data);
    } catch (err) {
      console.error("Failed to fetch graph:", err);
      setError("Failed to load network graph.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <h2>Network</h2>
        <p>Loading network graph...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <h2>Network</h2>
        <p className="error">{error}</p>
      </div>
    );
  }

  if (!graphData.nodes.length) {
    return (
      <div className="page-container">
        <h2>Network</h2>
        <p>No network data available.</p>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>Collaboration Network</h2>
        <p className="page-subtitle">
          Visualize student collaborations, startup founders, and connections.
        </p>
      </div>

      <div className="graph-container">
        <GraphView data={graphData} />
      </div>
    </div>
  );
}