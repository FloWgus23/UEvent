// frontend/src/services/authService.js
import apiClient from './api'

export default {
  // เข้าสู่ระบบ
  login(credentials) {
    return apiClient.post('/auth/login/', credentials)
  },

  // สมัครสมาชิก
  register(userData) {
    return apiClient.post('/auth/register/', userData)
  },

  // ดึงข้อมูลโปรไฟล์ (ใช้ /auth/me/ ตาม Backend)
  getUserProfile() {
    return apiClient.get('/auth/me/')
  },

  // ต่ออายุ Token
  refreshToken(token) {
    return apiClient.post('/auth/refresh/', { refresh: token })
  },

  // ⭐ เพิ่มฟังก์ชันนี้: ขอสิทธิ์เป็นผู้จัด
  // ⭐ แก้ไขฟังก์ชันนี้
  requestOrganizer(formData) {
    return apiClient.post('/auth/request-organizer/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data' // สำคัญมาก
      }
    })
  }
}