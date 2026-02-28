// frontend/src/api/startups.js

import client from "./client";

/**
 * ==========================================
 * STARTUP API
 * ==========================================
 */


/**
 * Get all startups
 */
export const getStartups = async () => {
  try {
    const response = await client.get("/startups");

    return response.data;
  } catch (error) {
    console.error("Failed to fetch startups:", error);
    throw error;
  }
};


/**
 * Get startup by ID
 */
export const getStartupById = async (startupId) => {
  try {
    const response = await client.get(
      `/startups/${startupId}`
    );

    return response.data;
  } catch (error) {
    console.error("Failed to fetch startup:", error);
    throw error;
  }
};


/**
 * Create new startup
 */
export const createStartup = async (startupData) => {
  try {
    const response = await client.post(
      "/startups",
      startupData
    );

    return response.data;
  } catch (error) {
    console.error("Failed to create startup:", error);
    throw error;
  }
};


/**
 * Update startup
 */
export const updateStartup = async (
  startupId,
  startupData
) => {
  try {
    const response = await client.put(
      `/startups/${startupId}`,
      startupData
    );

    return response.data;
  } catch (error) {
    console.error("Failed to update startup:", error);
    throw error;
  }
};


/**
 * Delete startup
 */
export const deleteStartup = async (startupId) => {
  try {
    const response = await client.delete(
      `/startups/${startupId}`
    );

    return response.data;
  } catch (error) {
    console.error("Failed to delete startup:", error);
    throw error;
  }
};