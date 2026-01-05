// frontend/src/services/activityService.js
import apiClient from './api.js'

export default {
  // ดึงกิจกรรมทั้งหมด
  getAllActivities(params = {}) {
    return apiClient.get('/activities/', { params })
  },

  // ⭐ ดึงเฉพาะกิจกรรมที่ตัวเองสร้าง (สำหรับ Organizer Dashboard)
  getMyActivities() {
    return apiClient.get('/activities/my_activities/')
  },

  // ดึงกิจกรรมตาม ID
  getActivity(id) {
    return apiClient.get(`/activities/${id}/`)
  },

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

  partialUpdateActivity(id, data) {
    return apiClient.patch(`/activities/${id}/`, data)
  },

  deleteActivity(id) {
    return apiClient.delete(`/activities/${id}/`)
  },

  uploadImage(id, file) {
    const formData = new FormData()
    formData.append('image', file)
    return apiClient.post(`/activities/${id}/upload-image/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  searchActivities(query) {
    return apiClient.get('/activities/', { params: { search: query } })
  },

  // ลงทะเบียนกิจกรรม
  registerActivity(activityId, userData) {
    return apiClient.post(`/activities/${activityId}/register/`, userData)
  },

  checkRegistration(activityId) {
    return apiClient.get(`/activities/${activityId}/check_registration/`)
  },

  unregisterActivity(activityId) {
    return apiClient.delete(`/activities/${activityId}/unregister/`)
  },

  getRegistrations(activityId) {
    return apiClient.get(`/activities/${activityId}/registrations/`)
  },

  getActivityRegistrations(activityId) {
    return apiClient.get(`/activities/${activityId}/registrations/`)
  },

  // ⭐ แก้ไขจุดนี้: เปลี่ยน URL ให้ตรงกับ urls.py ของ Backend
  getMyRegistrations() {
    // เดิม: return apiClient.get('/activities/my_registrations/') ❌ ผิด
    return apiClient.get('/my-registrations/') // ✅ ถูกต้อง
  },

  // กิจกรรมแนะนำ
  getRecommendedActivities() {
    return apiClient.get('/activities/recommended/')
  }
}