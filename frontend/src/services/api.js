// frontend/src/services/api.js
import axios from "axios";

/**
 * Base URL
 * - local  : http://127.0.0.1:8000
 * - prod   : https://uevent-production.up.railway.app
 */
const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// api root
const API_BASE_URL = `${BASE_URL}/api`;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/* =========================
   REQUEST INTERCEPTOR
   ========================= */
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

/* =========================
   RESPONSE INTERCEPTOR
   ========================= */
apiClient.interceptors.response.use(
  (response) => response,

  async (error) => {
    if (error.response?.status === 401) {
      console.warn("🔄 Access token หมดอายุ → refresh token");

      const refresh = localStorage.getItem("refresh");
      if (!refresh) {
        logout();
        return Promise.reject(error);
      }

      try {
        // 🔑 ขอ access token ใหม่
        const res = await axios.post(
          `${API_BASE_URL}/auth/refresh/`,
          { refresh }
        );

        localStorage.setItem("access", res.data.access);

        // ส่ง request เดิมซ้ำ
        error.config.headers.Authorization = `Bearer ${res.data.access}`;
        return apiClient(error.config);

      } catch (err) {
        console.error("❌ Refresh token หมดอายุ");
        logout();
      }
    }

    return Promise.reject(error);
  }
);

/* =========================
   LOGOUT HELPER
   ========================= */
function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  window.location.href = "/login";
}

// debug ดูตอนเดโม
console.log("🔗 API BASE URL:", API_BASE_URL);

export default apiClient;
