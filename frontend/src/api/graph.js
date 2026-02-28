// frontend/src/api/graph.js

import client from "./client";

/**
 * ==========================================
 * GRAPH API
 * ==========================================
 * Handles innovation ecosystem graph data
 */


/**
 * Fetch full graph data
 * Returns:
 * {
 *   nodes: [],
 *   edges: []
 * }
 */
export const getGraphData = async () => {
  try {
    const response = await client.get("/graph/graph-data");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch graph data:", error);
    throw error;
  }
};


/**
 * Optional future:
 * Fetch node recommendations
 */
export const getNodeRecommendations = async (entityId) => {
  try {
    const response = await client.get(
      `/recommendations/full/${entityId}`
    );

    return response.data;
  } catch (error) {
    console.error("Recommendation fetch failed:", error);
    throw error;
  }
};