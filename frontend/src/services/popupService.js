import api from "./api";

// api.js ใส่ "/api" ให้ใน baseURL แล้ว จึงไม่ต้องใส่ซ้ำ
export const getActivePopups = () =>
  api.get("/popups/active/").then((r) => r.data);

export const getPopupPreview = (token) =>
  api.get(`/popups/preview/${token}/`).then((r) => r.data);