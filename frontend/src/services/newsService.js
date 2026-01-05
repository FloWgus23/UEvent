// frontend/src/services/newsService.js
import apiClient from './api.js'

export default {
  // ดึงข่าวทั้งหมด
  getAllNews(params = {}) {
    return apiClient.get('/news/', { params })
      .then(response => {
        // ถ้า API ใช้ pagination จะมี results
        if (response.data.results) {
          return { ...response, data: response.data.results }
        }
        return response
      })
  },

  // ⭐ ดึงเฉพาะข่าวที่ตัวเองสร้าง (สำหรับ Organizer Dashboard)
  getMyNews() {
    return apiClient.get('/news/my_news/')
      .then(response => {
        // ถ้า API ใช้ pagination จะมี results
        if (response.data.results) {
          return { ...response, data: response.data.results }
        }
        return response
      })
  },

  // ดึงข่าวตาม ID
  getNews(id) {
    return apiClient.get(`/news/${id}/`)
  },

  // สร้างข่าวใหม่ (รองรับ FormData)
  createNews(data) {
    if (data instanceof FormData) {
      return apiClient.post('/news/', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } 
    return apiClient.post('/news/', data)
  },

  // อัปเดตข่าว (PATCH ถ้าเป็น FormData)
  updateNews(id, data) {
    if (data instanceof FormData) {
      return apiClient.patch(`/news/${id}/`, data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
    return apiClient.put(`/news/${id}/`, data)
  },

  // แก้ไขบางส่วน
  partialUpdateNews(id, data) {
    return apiClient.patch(`/news/${id}/`, data)
  },

  // ลบข่าว
  deleteNews(id) {
    return apiClient.delete(`/news/${id}/`)
  },

  // อัปโหลดรูปภาพข่าว
  uploadImage(id, file) {
    const formData = new FormData()
    formData.append('image', file)

    return apiClient.post(`/news/${id}/upload-image/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // ค้นหาข่าว
  searchNews(query) {
    return apiClient.get('/news/', {
      params: { search: query }
    })
    .then(response => {
      // ถ้า API ใช้ pagination จะมี results
      if (response.data.results) {
        return { ...response, data: response.data.results }
      }
      return response
    })
  }
}