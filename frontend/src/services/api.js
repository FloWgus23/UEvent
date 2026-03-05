// frontend/src/services/api.js
import axios from "axios";
//กำหนด URL หลักของ API
const API_BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000") + "/api";
//สร้างตัวแปร apiClient โดยมี baseURL และ headers
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ⭐ เพิ่ม JWT Access Token อัตโนมัติในทุก request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ⭐ เมื่อ access token หมดอายุ → ใช้ refresh token อัตโนมัติ
apiClient.interceptors.response.use(
  (response) => response,

  async (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("JWT Access Token expired → trying refresh...");

      const refresh = localStorage.getItem("refresh");

      if (!refresh) {
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        // ขอ access token ใหม่
        const res = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refresh,
        });

        // เก็บ access token ใหม่
        localStorage.setItem("access", res.data.access);

        // ส่ง request เดิมใหม่
        error.config.headers.Authorization = `Bearer ${res.data.access}`;
        return apiClient(error.config);

      } catch (err) {
        console.error("Refresh token หมดอายุ → ออกจากระบบ");
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
