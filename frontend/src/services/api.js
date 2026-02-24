import axios from "axios";

// ==========================================
// Environment configuration
// ==========================================
const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// ==========================================
// Axios instance
// ==========================================
const API = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// ==========================================
// Request interceptor (attach token)
// ==========================================
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ==========================================
// Response interceptor (handle errors)
// ==========================================
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      console.error("Network error:", error);
      return Promise.reject({
        message: "Network error. Please check backend.",
      });
    }

    const { status, data } = error.response;

    if (status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }

    return Promise.reject(data);
  }
);

// ==========================================
// Auth APIs
// ==========================================
export const AuthAPI = {
  register: (payload) => API.post("/auth/register", payload),

  login: async (payload) => {
    const response = await API.post("/auth/login", payload);

    if (response.data.access_token) {
      localStorage.setItem("access_token", response.data.access_token);
    }

    return response;
  },

  logout: () => {
    localStorage.removeItem("access_token");
  },

  getCurrentUser: () => API.get("/auth/me"),
};

// ==========================================
// Student APIs
// ==========================================
export const StudentAPI = {
  getAll: () => API.get("/students"),

  getById: (id) => API.get(`/students/${id}`),

  create: (data) => API.post("/students", data),

  update: (id, data) => API.put(`/students/${id}`, data),

  delete: (id) => API.delete(`/students/${id}`),
};

// ==========================================
// Mentor APIs
// ==========================================
export const MentorAPI = {
  getAll: () => API.get("/mentors"),

  getById: (id) => API.get(`/mentors/${id}`),
};

// ==========================================
// Startup APIs
// ==========================================
export const StartupAPI = {
  getAll: () => API.get("/startups"),

  getById: (id) => API.get(`/startups/${id}`),

  create: (data) => API.post("/startups", data),
};

// ==========================================
// Recommendation APIs
// ==========================================
export const RecommendationAPI = {
  getFull: (studentId) =>
    API.get(`/recommendations/${studentId}`),

  getStudents: (studentId) =>
    API.get(`/recommendations/students/${studentId}`),

  getMentors: (studentId) =>
    API.get(`/recommendations/mentors/${studentId}`),

  getStartups: (studentId) =>
    API.get(`/recommendations/startups/${studentId}`),
};

// ==========================================
// Graph APIs
// ==========================================
export const GraphAPI = {
  getGraph: () => API.get("/graph"),

  getTopInnovators: () => API.get("/graph/top-innovators"),
};

// ==========================================
// Achievement APIs
// ==========================================
export const AchievementAPI = {
  getByStudent: (studentId) =>
    API.get(`/achievements/student/${studentId}`),

  create: (data) =>
    API.post("/achievements", data),
};

// ==========================================
// Export base instance
// ==========================================
export default API;