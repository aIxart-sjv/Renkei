// src/utils/helpers.jsx

// -----------------------------------------
// API BASE URL
// -----------------------------------------
export const API_BASE =
  import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";


// -----------------------------------------
// GENERIC API REQUEST HANDLER
// -----------------------------------------
export async function apiRequest(
  endpoint,
  method = "GET",
  data = null,
  token = null
) {
  try {
    const headers = {
      "Content-Type": "application/json",
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
      method,
      headers,
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, config);

    // Handle HTTP errors
    if (!response.ok) {
      let errorMessage = "Something went wrong";

      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        errorMessage = response.statusText;
      }

      throw new Error(errorMessage);
    }

    // Handle empty response
    if (response.status === 204) {
      return null;
    }

    return await response.json();

  } catch (error) {
    console.error("API Error:", error.message);
    throw error;
  }
}


// -----------------------------------------
// AUTH HELPERS
// -----------------------------------------
export function saveToken(token) {
  localStorage.setItem("token", token);
}

export function getToken() {
  return localStorage.getItem("token");
}

export function removeToken() {
  localStorage.removeItem("token");
}

export function isAuthenticated() {
  return !!getToken();
}


// -----------------------------------------
// USER HELPERS
// -----------------------------------------
export function saveUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

export function getUser() {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

export function removeUser() {
  localStorage.removeItem("user");
}


// -----------------------------------------
// FORMATTERS
// -----------------------------------------
export function formatDate(dateString) {
  if (!dateString) return "";

  const date = new Date(dateString);

  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function formatScore(score) {
  if (score === undefined || score === null) return "0";
  return Number(score).toFixed(2);
}


// -----------------------------------------
// TEXT HELPERS
// -----------------------------------------
export function capitalize(text) {
  if (!text) return "";
  return text.charAt(0).toUpperCase() + text.slice(1);
}

export function truncate(text, maxLength = 100) {
  if (!text) return "";
  return text.length > maxLength
    ? text.substring(0, maxLength) + "..."
    : text;
}


// -----------------------------------------
// ARRAY HELPERS
// -----------------------------------------
export function uniqueArray(arr) {
  return [...new Set(arr)];
}

export function safeArray(arr) {
  return Array.isArray(arr) ? arr : [];
}


// -----------------------------------------
// ERROR HELPER
// -----------------------------------------
export function getErrorMessage(error) {
  if (!error) return "Unknown error";

  if (typeof error === "string") return error;

  if (error.message) return error.message;

  return "Something went wrong";
}


// -----------------------------------------
// GRAPH HELPERS
// -----------------------------------------
export function normalizeGraphData(data) {
  if (!data) {
    return {
      nodes: [],
      links: [],
    };
  }

  return {
    nodes: data.nodes || [],
    links: data.edges || [],
  };
}