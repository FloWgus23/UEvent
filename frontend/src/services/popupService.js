import api from "./api";   // ← เปลี่ยนเป็นไฟล์ axios ที่โปรเจคคุณมีอยู่แล้ว

export const getActivePopups = () =>
  api.get("/api/popups/active/").then((r) => r.data);

export const getPopupPreview = (token) =>
  api.get(`/api/popups/preview/${token}/`).then((r) => r.data);