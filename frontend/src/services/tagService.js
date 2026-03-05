// frontend/src/services/tagService.js
import apiClient from './api.js'

export default {
 
  /**
   * ดึง Tags ทั้งหมด (สำหรับแสดงใน Modal) * ดึง Tags ทั้งหมด
   * หน้าที่: เอามาโชว์ให้ User เลือกเยอะๆ (เช่น ในหน้า Modal ตอนเริ่มใช้งานครั้งแรก)
   * GET /api/tags/
   */
  getAllTags() {
    return apiClient.get('/tags/')
  },

  /**
   * ค้นหา Tags (สำหรับ Autocomplete)  ค้นหา Tags (Search / Autocomplete)
   * หน้าที่: เวลา User พิมพ์ในช่องค้นหา (เช่น พิมพ์ "IT") ก็จะส่งคำว่า "IT" ไปถามหลังบ้าน
   * GET /api/tags/search/?q=IT
   */
  searchTags(query) {
    return apiClient.get('/tags/search/', {
      params: { q: query }
    })
  },

  /**
   * ดึงความสนใจของ User ปัจจุบัน   ดูว่า User คนนี้ชอบอะไรบ้าง
   * หน้าที่: ดึงรายการ Tag ที่ User คนนี้เคยกดเลือกไว้
   * GET /api/user/interests/
   */
  getUserInterests() {
    return apiClient.get('/user/interests/')
  },

  /**
   * บันทึกความสนใจจาก Onboarding Modal  * บันทึกความสนใจ (ตอน Onboarding)
   * หน้าที่: ส่งรายการ Tag ที่ User เลือกไปบันทึกลง Database
   * POST /api/user/interests/
   * 
   * @param {Array} tags - [{ tag_id: 1, score: 5.0 }, ...]
   */
  saveUserInterests(tags) {
    return apiClient.post('/user/interests/', { tags })
  },

  /**
   * เช็คว่า User มีความสนใจหรือยัง
   * GET /api/user/has-interests/  * เช็คสถานะ: "เคยเลือกความสนใจหรือยัง?"
   * หน้าที่: ถามหลังบ้านว่า User คนนี้เป็นคนใหม่ซิงๆ หรือเคยเลือก Tag แล้ว
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
   * ดึงกิจกรรมแนะนำตามความสนใจ   * ดึงกิจกรรมแนะนำ (The Magic Function ✨)
   * หน้าที่: ขอรายการกิจกรรมที่ "เหมาะสมที่สุด" สำหรับ User คนนี้
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