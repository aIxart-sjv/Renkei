// frontend/src/api/mentors.js

import client from "./client";

/**
 * ==========================================
 * MENTOR API
 * ==========================================
 */


/**
 * Get all mentors
 */
export const getMentors = async () => {
  try {
    const response = await client.get("/mentors");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch mentors:", error);
    throw error;
  }
};


/**
 * Get mentor by ID
 */
export const getMentorById = async (mentorId) => {
  try {
    const response = await client.get(`/mentors/${mentorId}`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch mentor:", error);
    throw error;
  }
};


/**
 * Create mentor profile
 */
export const createMentor = async (mentorData) => {
  try {
    const response = await client.post(
      "/mentors",
      mentorData
    );

    return response.data;
  } catch (error) {
    console.error("Mentor creation failed:", error);
    throw error;
  }
};


/**
 * Update mentor profile
 */
export const updateMentor = async (mentorId, mentorData) => {
  try {
    const response = await client.put(
      `/mentors/${mentorId}`,
      mentorData
    );

    return response.data;
  } catch (error) {
    console.error("Mentor update failed:", error);
    throw error;
  }
};


/**
 * Delete mentor
 */
export const deleteMentor = async (mentorId) => {
  try {
    const response = await client.delete(
      `/mentors/${mentorId}`
    );

    return response.data;
  } catch (error) {
    console.error("Mentor deletion failed:", error);
    throw error;
  }
};