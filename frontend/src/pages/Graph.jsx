// frontend/src/pages/Graph.jsx

import { useEffect, useState } from "react";
import "./Graph.css";

import Navbar from "../components/common/Navbar";
import Sidebar from "../components/common/Sidebar";
import GraphView from "../components/graph/GraphView";

import { getGraphData } from "../api/graph";

const Graph = () => {

  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGraph();
  }, []);

  const fetchGraph = async () => {
    try {
      const data = await getGraphData();
      setGraphData(data);
    } catch (err) {
      console.error("Graph load failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="graph-layout">

      <Sidebar />

      <div className="graph-main">

        <Navbar />

        <div className="graph-container">

          {/* HEADER */}
          <div className="graph-header">
            <h1>Innovation Intelligence Graph</h1>
            <p>
              Visualizing collaboration, mentorship, and startup ecosystems
            </p>
          </div>

          {/* GRAPH PANEL */}
          <div className="graph-panel">

            {loading ? (
              <div className="graph-loading">
                Building innovation network...
              </div>
            ) : (
              <GraphView data={graphData} />
            )}

          </div>

        </div>

      </div>

    </div>
  );
};

export default Graph;