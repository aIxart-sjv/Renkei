import React, { useEffect, useState, useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";
import "./GraphView.css";

/**
 * GraphView Component
 * Visualizes campus collaboration graph
 * Production‑ready, clean, backend‑driven
 */
const GraphView = () => {
  const graphRef = useRef();
  const [graphData, setGraphData] = useState({
    nodes: [],
    links: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Fetch graph data from backend
   */
  const fetchGraphData = async () => {
    try {
      setLoading(true);

      const response = await fetch("http://127.0.0.1:8000/graph");

      if (!response.ok) {
        throw new Error("Failed to fetch graph data");
      }

      const data = await response.json();

      // Transform backend format to ForceGraph format
      const transformed = {
        nodes: data.nodes.map((node) => ({
          id: node.id,
          name: node.name,
          type: node.type || "student",
        })),
        links: data.edges.map((edge) => ({
          source: edge.source,
          target: edge.target,
          type: edge.type,
        })),
      };

      setGraphData(transformed);
      setError(null);
    } catch (err) {
      console.error("Graph fetch error:", err);
      setError("Unable to load graph data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraphData();
  }, []);

  /**
   * Node color based on type
   */
  const getNodeColor = (node) => {
    switch (node.type) {
      case "student":
        return "#4f46e5";
      case "mentor":
        return "#059669";
      case "startup":
        return "#dc2626";
      default:
        return "#6b7280";
    }
  };

  /**
   * Node label rendering
   */
  const drawNodeLabel = (node, ctx, globalScale) => {
    const label = node.name;
    const fontSize = 12 / globalScale;
    ctx.font = `${fontSize}px Inter, sans-serif`;

    ctx.fillStyle = "#111";
    ctx.fillText(label, node.x + 8, node.y + 4);
  };

  if (loading) {
    return (
      <div className="graph-container">
        <div className="graph-loading">Loading network graph...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="graph-container">
        <div className="graph-error">{error}</div>
      </div>
    );
  }

  return (
    <div className="graph-container">
      <div className="graph-header">
        <h2>Innovation Network</h2>
        <p>Visualizing collaboration across students and startups</p>
      </div>

      <ForceGraph2D
        ref={graphRef}
        graphData={graphData}
        nodeLabel="name"
        nodeColor={getNodeColor}
        nodeCanvasObject={drawNodeLabel}
        linkColor={() => "#9ca3af"}
        linkWidth={1.5}
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={0.005}
        cooldownTicks={100}
        onNodeClick={(node) => {
          console.log("Node clicked:", node);
        }}
      />
    </div>
  );
};

export default GraphView;