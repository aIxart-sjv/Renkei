import React, {
  createContext,
  useContext,
  useState,
  useEffect,
} from "react";

/**
 * =========================================
 * Auth Context
 * Renkei Production Auth System
 * =========================================
 */

export const AuthContext = createContext(null);

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";


/**
 * =========================================
 * Auth Provider
 * =========================================
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const [token, setToken] = useState(
    localStorage.getItem("renkei_token")
  );

  const [loading, setLoading] = useState(true);


  /**
   * =========================================
   * Load user on app start
   * =========================================
   */
  useEffect(() => {
    const initAuth = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          throw new Error("Invalid token");
        }

        const userData = await res.json();

        setUser(userData);

      } catch (error) {
        console.error("Auth init failed:", error);
        logout();
      } finally {
        setLoading(false);
      }
    };

    initAuth();

  }, [token]);


  /**
   * =========================================
   * Login
   * =========================================
   */
  const login = async (email, password) => {
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Login failed");
      }

      const data = await res.json();

      setToken(data.access_token);

      localStorage.setItem(
        "renkei_token",
        data.access_token
      );

      return {
        success: true,
      };

    } catch (error) {
      console.error("Login error:", error);

      return {
        success: false,
        error: error.message,
      };
    }
  };


  /**
   * =========================================
   * Register
   * =========================================
   */
  const register = async (userData) => {
    try {
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Registration failed");
      }

      return {
        success: true,
      };

    } catch (error) {
      console.error("Register error:", error);

      return {
        success: false,
        error: error.message,
      };
    }
  };


  /**
   * =========================================
   * Logout
   * =========================================
   */
  const logout = () => {
    setUser(null);
    setToken(null);

    localStorage.removeItem("renkei_token");
  };


  /**
   * =========================================
   * Authenticated Fetch Helper
   * =========================================
   */
  const authFetch = async (
    endpoint,
    options = {}
  ) => {
    try {
      const res = await fetch(
        `${API_BASE}${endpoint}`,
        {
          ...options,
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            ...options.headers,
          },
        }
      );

      if (res.status === 401) {
        logout();
        throw new Error("Session expired");
      }

      return res;

    } catch (error) {
      console.error("authFetch error:", error);
      throw error;
    }
  };


  /**
   * =========================================
   * Context Value
   * =========================================
   */
  const value = {
    user,
    token,
    loading,

    login,
    register,
    logout,

    authFetch,

    isAuthenticated: !!user,
  };


  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};


/**
 * =========================================
 * Auth Hook
 * =========================================
 */
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    )
  }

  return context;
};