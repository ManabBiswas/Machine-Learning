import axios from "axios";

// In dev, Vite proxies /api -> the FastAPI backend (see vite.config.ts).
// In prod, set VITE_API_URL to the deployed backend's base URL.
const baseURL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : "/api";

export const apiClient = axios.create({
  baseURL,
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.message ||
      "Something went wrong talking to the server.";
    return Promise.reject(new Error(message));
  }
);
