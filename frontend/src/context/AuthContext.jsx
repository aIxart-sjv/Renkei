import React, { createContext, useState, useEffect } from "react";
import { loginUser } from "../api/auth";
import api from "../api/client";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // ======================
  // RESTORE SESSION
  // ======================
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      api.defaults.headers.common["Authorization"] =
        `Bearer ${token}`;

      setUser({ authenticated: true });
    }

    setLoading(false);
  }, []);

  // ======================
  // LOGIN
  // ======================
  const login = async (username, password) => {
    const data = await loginUser(username, password);

    const token = data.access_token;

    localStorage.setItem("token", token);

    api.defaults.headers.common["Authorization"] =
      `Bearer ${token}`;

    setUser({ authenticated: true });
  };

  // ======================
  // LOGOUT
  // ======================
  const logout = () => {
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        loading,
        isAuthenticated: !!user
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};