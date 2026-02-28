// frontend/src/api/students.js

import client from "./client";

/**
 * ==========================================
 * STUDENT API
 * ==========================================
 */


/**
 * Get all students
 */
export const getStudents = async () => {
  try {
    const response = await client.get("/students");

    return response.data;
  } catch (error) {
    console.error("Failed to fetch students:", error);
    throw error;
  }
};


/**
 * Get student by ID
 */
export const getStudentById = async (studentId) => {
  try {
    const response = await client.get(
      `/students/${studentId}`
    );

    return response.data;
  } catch (error) {
    console.error("Failed to fetch student:", error);
    throw error;
  }
};


/**
 * Create student profile
 */
export const createStudent = async (studentData) => {
  try {
    const response = await client.post(
      "/students",
      studentData
    );

    return response.data;
  } catch (error) {
    console.error("Failed to create student:", error);
    throw error;
  }
};


/**
 * Update student profile
 */
export const updateStudent = async (
  studentId,
  studentData
) => {
  try {
    const response = await client.put(
      `/students/${studentId}`,
      studentData
    );

    return response.data;
  } catch (error) {
    console.error("Failed to update student:", error);
    throw error;
  }
};


/**
 * Delete student
 */
export const deleteStudent = async (studentId) => {
  try {
    const response = await client.delete(
      `/students/${studentId}`
    );

    return response.data;
  } catch (error) {
    console.error("Failed to delete student:", error);
    throw error;
  }
};