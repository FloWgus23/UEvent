// frontend/src/services/notificationService.js
import apiClient from './api'

export default {
  getMyNotifications() {
    return apiClient.get('/notifications/')
  },
  
  // อ่านทีละอัน
  markAsRead(id) {
    return apiClient.post(`/notifications/${id}/read/`)
  },
  
  // ⭐ แก้ไขชื่อฟังก์ชันเป็น markAllRead (ตัด As ออก) ให้ตรงกับที่เรียกใช้
  markAllRead() {
    return apiClient.post('/notifications/mark_all_read/')
  }
}