// frontend/src/services/tagService.js
import apiClient from './api.js'

export default {
  // ========================================
  // TAG APIS
  // ========================================
  
  /**
   * ดึง Tags ทั้งหมด (สำหรับแสดงใน Modal)
   * GET /api/tags/
   */
  getAllTags() {
    return apiClient.get('/tags/')
  },

  /**
   * ค้นหา Tags (สำหรับ Autocomplete)
   * GET /api/tags/search/?q=IT
   */
  searchTags(query) {
    return apiClient.get('/tags/search/', {
      params: { q: query }
    })
  },

  // ========================================
  // USER INTEREST APIS
  // ========================================

  /**
   * ดึงความสนใจของ User ปัจจุบัน
   * GET /api/user/interests/
   */
  getUserInterests() {
    return apiClient.get('/user/interests/')
  },

  /**
   * บันทึกความสนใจจาก Onboarding Modal
   * POST /api/user/interests/
   * 
   * @param {Array} tags - [{ tag_id: 1, score: 5.0 }, ...]
   */
  saveUserInterests(tags) {
    return apiClient.post('/user/interests/', { tags })
  },

  /**
   * เช็คว่า User มีความสนใจหรือยัง
   * GET /api/user/has-interests/
   * 
   * @returns {Promise<{has_interests: boolean}>}
   */
  checkUserHasInterests() {
    return apiClient.get('/user/has-interests/')
  },

  // ========================================
  // RECOMMENDATION APIS
  // ========================================

  /**
   * ดึงกิจกรรมแนะนำตามความสนใจ
   * GET /api/activities/recommended/
   * 
   * @returns {Promise<{
   *   activities: Array,
   *   recommendation_type: 'personalized' | 'popular',
   *   has_interests: boolean,
   *   message: string | null
   * }>}
   */
  getRecommendedActivities() {
    return apiClient.get('/activities/recommended/')
  }
}