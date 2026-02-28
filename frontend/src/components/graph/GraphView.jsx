// frontend/src/components/graph/GraphView.jsx

import React, { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

import { getGraphData } from "../../api/graph";

const GraphView = () => {

  const [graphData, setGraphData] = useState({
    nodes: [],
    edges: []
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // =============================
  // FETCH GRAPH
  // =============================
  useEffect(() => {

    const fetchGraph = async () => {
      try {

        const data = await getGraphData();

        setGraphData({
          nodes: data.nodes || [],
          links: data.edges || []
        });

      } catch (err) {
        console.error(err);
        setError("Failed to load graph");
      } finally {
        setLoading(false);
      }
    };

    fetchGraph();

  }, []);

  // =============================
  // STATES
  // =============================
  if (loading)
    return <div className="p-6">Loading graph...</div>;

  if (error)
    return <div className="p-6 text-red-500">{error}</div>;

  // =============================
  // NODE COLOR LOGIC
  // =============================
  const nodeColor = node => {
    switch (node.type) {
      case "student":
        return "#6366f1";
      case "mentor":
        return "#10b981";
      case "startup":
        return "#f59e0b";
      case "alumni":
        return "#ef4444";
      default:
        return "#9ca3af";
    }
  };

  // =============================
  // GRAPH RENDER
  // =============================
  return (
    <div className="w-full h-[85vh] bg-white rounded-xl shadow">

      <ForceGraph2D
        graphData={graphData}
        nodeLabel="label"
        nodeAutoColorBy="type"

        nodeCanvasObject={(node, ctx, globalScale) => {

          const label = node.label || node.id;
          const fontSize = 12 / globalScale;

          ctx.font = `${fontSize}px Sans-Serif`;

          ctx.fillStyle = nodeColor(node);
          ctx.beginPath();
          ctx.arc(node.x, node.y, 6, 0, 2 * Math.PI);
          ctx.fill();

          ctx.fillStyle = "#111";
          ctx.fillText(
            label,
            node.x + 8,
            node.y + 3
          );
        }}

        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={0.004}

        cooldownTicks={100}
      />

    </div>
  );
};

export default GraphView;