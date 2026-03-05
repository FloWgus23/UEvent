<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 font-sans">
    
    <header class="bg-blue-900/50 backdrop-blur-sm shadow-lg border-b border-white/10 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
        <h1 class="text-white text-2xl font-bold flex items-center gap-3">
          <i class="fa-solid fa-calendar-star text-2xl drop-shadow-md"></i>
          UEvent <span class="text-xs font-semibold uppercase tracking-widest bg-white/10 px-2 py-1 rounded-md text-blue-100">Organizer</span>
        </h1>
        <div class="flex items-center gap-4">
          <router-link to="/organizer/dashboard" class="text-blue-100 hover:text-white transition-colors text-sm font-medium flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-white/10">
            <i class="fa-solid fa-arrow-left"></i> กลับหน้าแดชบอร์ด
          </router-link>
        </div>
      </div>
    </header>

    <div class="max-w-4xl mx-auto px-6 py-12">
      <div class="bg-white rounded-[24px] shadow-2xl p-8 md:p-10 animate-fade-up">
        
        <div class="flex items-center gap-4 mb-8 pb-6 border-b border-gray-100">
           <div class="w-12 h-12 bg-yellow-100 rounded-2xl flex items-center justify-center text-yellow-600 shadow-sm">
              <i class="fa-solid fa-pen-to-square text-xl"></i>
           </div>
           <div>
              <h2 class="text-3xl font-bold text-gray-800">แก้ไขกิจกรรม</h2>
              <p class="text-gray-500 text-sm mt-1">ปรับปรุงข้อมูลกิจกรรมของคุณให้เป็นปัจจุบัน</p>
           </div>
        </div>

        <div v-if="isLoading" class="text-center py-20">
          <div class="inline-block w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
          <p class="text-gray-500 text-lg">กำลังโหลดข้อมูล...</p>
        </div>

        <form v-else @submit.prevent="handleSubmit" class="space-y-8">
          
          <div class="space-y-6">
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">ชื่อกิจกรรม <span class="text-red-500">*</span></label>
              <input 
                v-model="formData.name" 
                type="text" 
                class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-gray-800 font-medium" 
                required 
              />
            </div>

            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">รายละเอียด <span class="text-red-500">*</span></label>
              <textarea 
                v-model="formData.description" 
                rows="5" 
                class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-gray-800 resize-none leading-relaxed" 
                required
              ></textarea>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">วันที่จัด <span class="text-red-500">*</span></label>
              <input v-model="formData.date" type="date" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition-all" required />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">เวลาเริ่มต้น</label>
              <input v-model="formData.start_time" type="time" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition-all" />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">เวลาสิ้นสุด</label>
              <input v-model="formData.end_time" type="time" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition-all" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">จำนวนรับ (คน) <span class="text-red-500">*</span></label>
              <input v-model="formData.capacity" type="number" min="1" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition-all" required />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">หมวดหมู่หลัก <span class="text-red-500">*</span></label>
              <div class="relative">
                <select v-model="formData.category" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl appearance-none cursor-pointer focus:ring-2 focus:ring-blue-500 transition-all" required>
                  <option value="" disabled>-- เลือกหมวดหมู่ --</option>
                  <option value="academic">วิชาการและการเรียนรู้</option>
                  <option value="technology">เทคโนโลยีและนวัตกรรม</option>
                  <option value="entertainment">บันเทิงและนันทนาการ</option>
                  <option value="sports">กีฬาและสุขภาพ</option>
                  <option value="volunteer">จิตอาสาและสังคม</option>
                  <option value="career">แนะแนวและอาชีพ</option>
                  <option value="other">อื่นๆ</option>
                </select>
                <i class="fa-solid fa-chevron-down absolute right-4 top-4 text-gray-400 pointer-events-none"></i>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">สถานที่ <span class="text-red-500">*</span></label>
              <input v-model="formData.location" type="text" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition-all" required />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">หน่วยงานผู้จัด <span class="text-red-500">*</span></label>
              <input v-model="formData.organizer" type="text" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition-all" required />
            </div>
          </div>

          <div>
            <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">สถานะกิจกรรม</label>
            <div class="relative">
              <select v-model="formData.status" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl appearance-none cursor-pointer focus:ring-2 focus:ring-blue-500 transition-all">
                <option value="กำลังรับสมัคร">🟢 กำลังรับสมัคร</option>
                <option value="กำลังดำเนินการ">🔵 กำลังดำเนินการ</option>
                <option value="สิ้นสุดแล้ว">🔴 สิ้นสุดแล้ว</option>
                <option value="cancelled">❌ ยกเลิกกิจกรรม</option>
              </select>
              <i class="fa-solid fa-chevron-down absolute right-4 top-4 text-gray-400 pointer-events-none"></i>
            </div>
          </div>

          <div class="bg-blue-50/50 p-6 rounded-2xl border border-blue-100">
            <div class="flex justify-between items-center mb-4">
              <label class="block text-gray-800 font-bold text-lg flex items-center gap-2">
                <i class="fa-solid fa-tags text-blue-500"></i> แท็กที่เกี่ยวข้อง 
              </label>
              <span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold shadow-sm" v-if="selectedTagIds.length > 0">
                เลือกแล้ว {{ selectedTagIds.length }} รายการ
              </span>
            </div>
            
            <div v-if="availableTags.length === 0" class="text-center py-8 text-gray-400">
              <i class="fa-solid fa-circle-notch fa-spin"></i> กำลังโหลดข้อมูล...
            </div>
            
            <div v-else class="space-y-6 max-h-[400px] overflow-y-auto custom-scrollbar pr-2">
              <div v-for="(groupTags, groupName) in groupedTags" :key="groupName" class="bg-white p-4 rounded-xl border border-gray-200/60 shadow-sm">
                <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span> {{ groupName }}
                </h3>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="tag in groupTags"
                    :key="tag.id"
                    type="button"
                    @click="toggleTag(tag.id)"
                    class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 border flex items-center gap-2"
                    :class="selectedTagIds.includes(tag.id)
                      ? 'bg-blue-600 text-white border-blue-600 shadow-md transform scale-[1.02] ring-2 ring-blue-200'
                      : 'bg-gray-50 text-gray-600 border-gray-200 hover:border-blue-400 hover:text-blue-600 hover:bg-white'"
                  >
                    <span class="text-base">{{ tag.icon }}</span>
                    {{ tag.name }}
                    <i v-if="selectedTagIds.includes(tag.id)" class="fa-solid fa-check text-xs ml-1 bg-white/20 rounded-full p-0.5 w-4 h-4 flex items-center justify-center"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">รูปภาพปก</label>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
              <div v-if="currentImage" class="relative group">
                <p class="text-xs text-gray-500 mb-2 font-medium">รูปปัจจุบัน</p>
                <div class="relative w-full h-48 rounded-xl overflow-hidden border-2 border-gray-200 shadow-sm">
                    <img :src="currentImage" class="w-full h-full object-cover" @error="handleImageError">
                </div>
              </div>
              
              <div v-if="previewImage" class="relative animate-fade-in">
                <p class="text-xs text-green-600 mb-2 font-medium">รูปใหม่ที่จะใช้</p>
                <div class="relative w-full h-48 rounded-xl overflow-hidden border-2 border-green-400 shadow-md ring-2 ring-green-100">
                    <img :src="previewImage" class="w-full h-full object-cover">
                    <button @click="clearImage" type="button" class="absolute top-2 right-2 bg-red-500 text-white p-1.5 rounded-full shadow-lg hover:bg-red-600 transition">
                        <i class="fa-solid fa-xmark w-4 h-4 flex items-center justify-center text-xs"></i>
                    </button>
                </div>
              </div>
            </div>
            
            <div class="flex items-center gap-4 p-6 border-2 border-dashed border-gray-300 rounded-2xl bg-gray-50 hover:bg-blue-50 hover:border-blue-300 transition group cursor-pointer" @click="$refs.fileInput.click()">
              <div class="w-12 h-12 bg-white border border-gray-200 rounded-full flex items-center justify-center shadow-sm group-hover:scale-110 transition-transform">
                <i class="fa-solid fa-cloud-arrow-up text-blue-500 text-xl"></i>
              </div>
              <div>
                <p class="font-medium text-gray-700 group-hover:text-blue-700 transition-colors">คลิกเพื่ออัปโหลดรูปภาพใหม่</p>
                <p class="text-xs text-gray-500 mt-1">{{ imageFileName || 'รองรับ JPG, PNG (ไม่เกิน 5MB)' }}</p>
              </div>
              <input id="image" ref="fileInput" type="file" accept="image/*" @change="handleImageUpload" class="hidden" />
            </div>
          </div>

          <div class="flex flex-col md:flex-row gap-4 pt-8 border-t border-gray-100 mt-8">
            <button 
              type="submit" 
              :disabled="isSaving" 
              class="flex-1 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold text-lg shadow-lg shadow-blue-200 transition-all transform hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <i v-if="isSaving" class="fa-solid fa-circle-notch fa-spin"></i>
              <span v-else><i class="fa-solid fa-save"></i> บันทึกการแก้ไข</span>
            </button>
            
            <button 
              type="button" 
              @click="handleCancel" 
              :disabled="isSaving" 
              class="px-8 py-4 bg-white border-2 border-gray-200 text-gray-600 hover:text-red-600 hover:border-red-200 hover:bg-red-50 rounded-xl font-semibold transition-all disabled:opacity-50"
            >
              ยกเลิก
            </button>
          </div>

        </form>
      </div>
    </div>

    <footer class="bg-blue-900/50 backdrop-blur-sm text-white py-8 mt-12 text-center border-t border-white/10">
      <div class="flex items-center justify-center gap-2 mb-2 opacity-80">
        <i class="fa-solid fa-calendar-star"></i>
        <span class="font-bold">UEvent Organizer</span>
      </div>
      <p class="text-sm opacity-60">© 2025 All Rights Reserved</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import activityService from '@/services/activityService.js'
import tagService from '@/services/tagService.js'

const router = useRouter()
const route = useRoute()

const activityId = ref(route.params.id)
const isLoading = ref(false)
const isSaving = ref(false)

// State
const availableTags = ref([])
const selectedTagIds = ref([]) 
const formData = ref({
  name: '', description: '', date: '', start_time: '', end_time: '',
  capacity: '', location: '', organizer: '', category: '', status: 'กำลังรับสมัคร'
})

const imageFile = ref(null)
const imageFileName = ref('')
const currentImage = ref('')
const previewImage = ref('')
const fileInput = ref(null)

// Fallback Tags
const FALLBACK_TAGS = [
  { id: 1, name: 'เขียนโปรแกรม', icon: '💻' },
  { id: 2, name: 'AI และข้อมูล', icon: '🤖' },
  { id: 3, name: 'นวัตกรรม', icon: '💡' },
  { id: 4, name: 'วิทยาศาสตร์', icon: '🔬' },
  { id: 5, name: 'ออกแบบ', icon: '🎨' },
  { id: 6, name: 'สื่อ/มีเดีย', icon: '🎬' },
  { id: 7, name: 'ภาษา', icon: '🗣️' },
  { id: 8, name: 'ติวสอบ', icon: '📚' },
  { id: 9, name: 'บริหารธุรกิจ', icon: '💼' },
  { id: 10, name: 'การตลาด', icon: '📈' },
  { id: 14, name: 'กฎหมาย/สังคม', icon: '⚖️' },
  { id: 17, name: 'สุขภาพ', icon: '🩺' },
  { id: 19, name: 'กีฬา', icon: '⚽' },
  { id: 23, name: 'ดนตรี', icon: '🎵' },
  { id: 27, name: 'เกม', icon: '🎮' },
  { id: 34, name: 'จิตอาสา', icon: '🤝' },
  { id: 40, name: 'การแข่งขัน', icon: '🥇' }
]

// Grouped Tags Logic
const groupedTags = computed(() => {
  const groups = {
    '🎓 วิชาการ & ทักษะ': ['เขียนโปรแกรม', 'AI และข้อมูล', 'นวัตกรรม', 'วิทยาศาสตร์', 'ออกแบบ', 'สื่อ/มีเดีย', 'ภาษา', 'ติวสอบ'],
    '💼 ธุรกิจ & สังคม': ['บริหารธุรกิจ', 'การตลาด', 'การเงิน/หุ้น', 'สตาร์ทอัพ', 'หางาน/ฝึกงาน', 'กฎหมาย/สังคม', 'ภาวะผู้นำ', 'เสวนา/บรรยาย'],
    '🧘‍♂️ สุขภาพ & กีฬา': ['สุขภาพ', 'สุขภาพจิต', 'กีฬา', 'วิ่ง', 'ฟิตเนส', 'เกษตร/ธรรมชาติ'],
    '🎉 บันเทิง & ไลฟ์สไตล์': ['ดนตรี', 'ภาพยนตร์', 'ศิลปะ', 'ถ่ายภาพ', 'เกม', 'บอร์ดเกม', 'ท่องเที่ยว', 'อาหาร', 'แฟชั่น', 'สัตว์เลี้ยง', 'มูเตลู'],
    '🤝 กิจกรรม & จิตอาสา': ['จิตอาสา', 'ค่ายอาสา', 'สิ่งแวดล้อม', 'รับน้อง', 'วัฒนธรรม', 'เวิร์กชอป', 'การแข่งขัน']
  }

  const result = {}
  Object.keys(groups).forEach(key => result[key] = [])
  result['📌 อื่นๆ'] = []

  availableTags.value.forEach(tag => {
    let placed = false
    for (const [groupName, keywords] of Object.entries(groups)) {
      if (keywords.includes(tag.name)) {
        result[groupName].push(tag)
        placed = true
        break
      }
    }
    if (!placed) result['📌 อื่นๆ'].push(tag)
  })

  return Object.fromEntries(Object.entries(result).filter(([_, tags]) => tags.length > 0))
})

const fetchTags = async () => {
  try {
    const res = await tagService.getAllTags()
    availableTags.value = res.data && res.data.length > 0 ? res.data : FALLBACK_TAGS
  } catch (error) {
    availableTags.value = FALLBACK_TAGS
  }
}

const toggleTag = (id) => {
  const index = selectedTagIds.value.indexOf(id)
  if (index === -1) selectedTagIds.value.push(id)
  else selectedTagIds.value.splice(index, 1)
}

const fetchActivity = async () => {
  try {
    isLoading.value = true
    const response = await activityService.getActivity(activityId.value)
    const activity = response.data
    
    formData.value = {
      name: activity.name,
      description: activity.description,
      date: activity.date,
      start_time: activity.start_time || '',
      end_time: activity.end_time || '',
      capacity: activity.capacity,
      location: activity.location,
      organizer: activity.organizer,
      category: activity.category,
      status: activity.status
    }
    
    if (activity.image) currentImage.value = activity.image

    // Map Tags
    if (activity.tag_list && Array.isArray(activity.tag_list)) {
      selectedTagIds.value = activity.tag_list.map(t => t.id)
    } else if (activity.tags && Array.isArray(activity.tags)) {
      selectedTagIds.value = activity.tags
    }

  } catch (error) {
    console.error('Error:', error)
    alert('ไม่สามารถโหลดข้อมูลได้')
    router.push('/organizer/dashboard')
  } finally {
    isLoading.value = false
  }
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
    if (!validTypes.includes(file.type)) return alert('กรุณาเลือกไฟล์รูปภาพเท่านั้น')
    if (file.size > 5 * 1024 * 1024) return alert('ขนาดไฟล์ต้องไม่เกิน 5MB')
    
    imageFile.value = file
    imageFileName.value = file.name
    const reader = new FileReader()
    reader.onload = (e) => { previewImage.value = e.target.result }
    reader.readAsDataURL(file)
  }
}

const clearImage = () => {
  imageFile.value = null
  imageFileName.value = ''
  previewImage.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/400x300?text=Image+Not+Found'
}

// ⭐ Fixed handleSubmit: ใช้ FormData เสมอ เพื่อความชัวร์และรองรับการส่งรูปภาพ+แท็ก
const handleSubmit = async () => {
  try {
    if (formData.value.start_time && formData.value.end_time) {
      if (formData.value.end_time <= formData.value.start_time) return alert('เวลาสิ้นสุดต้องมากกว่าเวลาเริ่มต้น')
    }

    isSaving.value = true

    // ใช้ FormData เสมอ เพื่อความปลอดภัยในการส่งข้อมูล
    const payload = new FormData()
    
    // Append fields
    Object.keys(formData.value).forEach(key => {
      if (formData.value[key] !== null && formData.value[key] !== undefined) {
        payload.append(key, formData.value[key])
      }
    })

    // Append Image
    if (imageFile.value) {
      payload.append('image', imageFile.value)
    }

    // Append Tags (สำคัญ: ต้องวนลูป append)
    selectedTagIds.value.forEach(id => {
      payload.append('tag_ids', id)
    })

    // ส่งแบบ PATCH (ใน Service เขียนรองรับ FormData ไว้แล้ว)
    await activityService.updateActivity(activityId.value, payload)
    
    alert('✅ บันทึกการแก้ไขสำเร็จ!')
    router.push('/organizer/dashboard')

  } catch (error) {
    console.error('Error:', error)
    alert('❌ เกิดข้อผิดพลาด: ' + (error.response?.data?.detail || error.message))
  } finally {
    isSaving.value = false
  }
}

const handleCancel = () => {
  if (confirm('ต้องการยกเลิกการแก้ไขหรือไม่?')) router.push('/organizer/dashboard')
}

onMounted(() => {
  fetchTags()
  fetchActivity()
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.animate-fade-up { animation: fadeUp 0.5s ease-out; }
.animate-fade-in { animation: fadeIn 0.3s ease-out; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>