import api from "./client";

// LOGIN
export const loginUser = async (username, password) => {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);

  const res = await api.post(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded"
      }
    }
  );

  return res.data;
};

// REGISTER
export const registerUser = async (data) => {
  const res = await api.post(
    "/auth/register",
    data
  );

  return res.data;
};