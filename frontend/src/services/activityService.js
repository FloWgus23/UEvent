// frontend/src/services/activityService.js
import apiClient from './api.js'

export default {
  // ดึงกิจกรรมทั้งหมด  (เอามาโชว์หน้าแรก)
  getAllActivities(params = {}) {
    return apiClient.get('/activities/', { params })
  },

  // ดึงเฉพาะกิจกรรมที่ตัวเองสร้าง (สำหรับ Organizer Dashboard)
  getMyActivities() {
    return apiClient.get('/activities/my_activities/')
  },

  // ดึงกิจกรรมตาม ID 1 อัน
  getActivity(id) {
    return apiClient.get(`/activities/${id}/`)
  },
   // ทำงานได้เหมือนกับ getActivity(id)
  getActivityById(id) {
    return apiClient.get(`/activities/${id}/`)
  },

  // สร้างกิจกรรมใหม่
  createActivity(data) {
    if (data instanceof FormData) {
      return apiClient.post('/activities/', data, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      return apiClient.post('/activities/', data)
    }
  },

  // อัปเดตกิจกรรม
  updateActivity(id, data) {
    if (data instanceof FormData) {
      return apiClient.patch(`/activities/${id}/`, data, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      return apiClient.put(`/activities/${id}/`, data)
    }
  },
  
  // แก้ไขบางส่วน (แบบเจาะจงใช้ PATCH)
  partialUpdateActivity(id, data) {
    return apiClient.patch(`/activities/${id}/`, data)
  },
  
  // ลบกิจกรรมทิ้ง
  deleteActivity(id) {
    return apiClient.delete(`/activities/${id}/`)
  },
  
  // อัปโหลดรูปภาพกิจกรรม (แยกออกมาเฉพาะทาง)
  uploadImage(id, file) {
    const formData = new FormData()
    formData.append('image', file)
    return apiClient.post(`/activities/${id}/upload-image/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  // ค้นหากิจกรรม (Search Bar)
  searchActivities(query) {
    return apiClient.get('/activities/', { params: { search: query } })
  },

  // ลงทะเบียนกิจกรรม
  registerActivity(activityId, userData) {
    return apiClient.post(`/activities/${activityId}/register/`, userData)
  },
  
  // เช็คว่า "ฉันลงทะเบียนกิจกรรมนี้ไปหรือยัง?" (เอาไว้เปลี่ยนปุ่มจาก "เข้าร่วม" เป็น "ลงทะเบียนแล้ว")
  checkRegistration(activityId) {
    return apiClient.get(`/activities/${activityId}/check_registration/`)
  },
  
  // กดยกเลิกการเข้าร่วม (Unregister)
  unregisterActivity(activityId) {
    return apiClient.delete(`/activities/${activityId}/unregister/`)
  },
  
  // ดูรายชื่อคนที่มาลงทะเบียนกิจกรรมนี้ (Organizer เอาไว้เช็คชื่อ)
  // หมายเหตุ: 2 ฟังก์ชันนี้ซ้ำกัน เลือกใช้สักอันครับ
  getRegistrations(activityId) {
    return apiClient.get(`/activities/${activityId}/registrations/`)
  },

  getActivityRegistrations(activityId) {
    return apiClient.get(`/activities/${activityId}/registrations/`)
  },

  // ดูประวัติการเข้าร่วมกิจกรรมของฉัน
  getMyRegistrations() { 
    return apiClient.get('/my-registrations/') 
  },

  // กิจกรรมแนะนำ แนะนำกิจกรรมที่น่าสนใจ (Recommended)
  getRecommendedActivities() {
    return apiClient.get('/activities/recommended/')
  }
}