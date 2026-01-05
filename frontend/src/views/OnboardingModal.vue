<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto animate-fade-in">
    <div class="fixed inset-0 bg-blue-900/60 backdrop-blur-md transition-opacity"></div>

    <div class="flex min-h-full items-center justify-center p-4 md:p-6">
      <div class="relative bg-white rounded-[2rem] shadow-2xl max-w-4xl w-full overflow-hidden animate-slide-up border border-white/50">
        
        <div class="absolute top-0 left-0 w-full h-64 bg-gradient-to-b from-blue-50 to-white pointer-events-none"></div>
        <div class="absolute -top-24 -right-24 w-64 h-64 bg-blue-100 rounded-full blur-3xl opacity-60 pointer-events-none"></div>
        <div class="absolute top-10 -left-20 w-40 h-40 bg-indigo-100 rounded-full blur-3xl opacity-60 pointer-events-none"></div>

        <div class="relative p-8 md:p-12">
          
          <div class="text-center mb-10 animate-fade-in-up">
            <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full mb-6 text-sm font-semibold shadow-sm">
              <i class="fa-solid fa-sparkles"></i>
              <span>ยินดีต้อนรับสู่ UEvent</span>
            </div>

            <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4 tracking-tight">
              เลือกสิ่งที่คุณ <span class="text-blue-600">สนใจ</span>
            </h1>
            <p class="text-lg text-gray-500 font-light max-w-lg mx-auto">
              เลือกหัวข้อที่คุณชอบอย่างน้อย 1 รายการ เพื่อให้เราคัดสรรกิจกรรมที่โดนใจคุณที่สุด
            </p>
          </div>

          <div v-if="loading" class="text-center py-20 animate-fade-in">
            <div class="w-12 h-12 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p class="text-gray-400">กำลังเตรียมข้อมูล...</p>
          </div>

          <div v-else class="animate-fade-in-up-delay">
            
            <div class="flex flex-col md:flex-row gap-4 mb-8">
              <div class="relative flex-1 group">
                <i class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-blue-500 transition-colors"></i>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="ค้นหาความสนใจ (เช่น กีฬา, ดนตรี...)"
                  class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-gray-700"
                />
              </div>
              
              <div class="flex items-center justify-center px-5 py-3 bg-blue-50 rounded-xl text-blue-800 font-medium whitespace-nowrap border border-blue-100">
                <span class="mr-2 text-2xl font-bold">{{ selectedTags.length }}</span> รายการที่เลือก
              </div>
            </div>

            <div class="max-h-[400px] overflow-y-auto custom-scrollbar pr-2 -mr-2">
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                <button
                  v-for="(tag, index) in filteredTags"
                  :key="tag.id"
                  @click="toggleTag(tag.id)"
                  :style="{ animationDelay: `${index * 30}ms` }"
                  class="relative group p-4 rounded-2xl border-2 transition-all duration-200 flex flex-col items-center justify-center gap-3 text-center animate-scale-in"
                  :class="selectedTags.includes(tag.id)
                    ? 'border-blue-500 bg-blue-50 text-blue-700 shadow-md transform scale-[0.98]'
                    : 'border-gray-100 bg-white hover:border-blue-200 hover:shadow-lg hover:-translate-y-1 text-gray-600'"
                >
                  <div class="text-4xl group-hover:scale-110 transition-transform duration-300">
                    {{ tag.icon || '🏷️' }}
                  </div>
                  
                  <span class="font-bold text-sm md:text-base">{{ tag.name }}</span>

                  <div v-if="selectedTags.includes(tag.id)" class="absolute top-2 right-2 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-sm animate-check-pop">
                    <i class="fa-solid fa-check text-xs"></i>
                  </div>
                </button>
              </div>

              <div v-if="filteredTags.length === 0" class="text-center py-16">
                <div class="text-5xl mb-4 opacity-20">🤔</div>
                <p class="text-gray-400">ไม่พบหัวข้อที่ค้นหา</p>
              </div>
            </div>
          </div>

          <div class="mt-10 flex gap-4 pt-6 border-t border-gray-100">
            <button
              @click="skip"
              class="px-6 py-3.5 text-gray-500 hover:text-gray-800 hover:bg-gray-100 rounded-xl font-semibold transition-colors"
            >
              ข้ามไปก่อน
            </button>
            
            <button
              @click="submit"
              :disabled="selectedTags.length === 0 || saving"
              class="flex-1 px-6 py-3.5 rounded-xl font-bold text-lg shadow-lg transition-all transform flex items-center justify-center gap-2"
              :class="selectedTags.length > 0 && !saving
                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:shadow-blue-500/30 hover:scale-[1.02] active:scale-[0.98]'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'"
            >
              <i v-if="saving" class="fa-solid fa-circle-notch fa-spin"></i>
              <span v-else>บันทึกและเริ่มใช้งาน</span>
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import tagService from '@/services/tagService'

const isOpen = ref(false)
const tags = ref([])
const selectedTags = ref([])
const loading = ref(false)
const saving = ref(false)
const searchQuery = ref('')

// ⭐ MOCK_TAGS ภาษาไทย (40 รายการ)
const MOCK_TAGS = [
  // 🎓 หมวดวิชาการ
  { id: 1, name: 'เขียนโปรแกรม', icon: '💻' },
  { id: 2, name: 'AI และข้อมูล', icon: '🤖' },
  { id: 3, name: 'นวัตกรรม', icon: '💡' },
  { id: 4, name: 'วิทยาศาสตร์', icon: '🔬' },
  { id: 5, name: 'ออกแบบ', icon: '🎨' },
  { id: 6, name: 'สื่อ/มีเดีย', icon: '🎬' },
  { id: 7, name: 'ภาษา', icon: '🗣️' },
  { id: 8, name: 'ติวสอบ', icon: '📚' },

  // 💼 หมวดธุรกิจ & สังคม
  { id: 9, name: 'บริหารธุรกิจ', icon: '💼' },
  { id: 10, name: 'การตลาด', icon: '📈' },
  { id: 11, name: 'การเงิน/หุ้น', icon: '💰' },
  { id: 12, name: 'สตาร์ทอัพ', icon: '🚀' },
  { id: 13, name: 'หางาน/ฝึกงาน', icon: '👔' },
  { id: 14, name: 'กฎหมาย/สังคม', icon: '⚖️' },
  { id: 15, name: 'ภาวะผู้นำ', icon: '🏆' },
  { id: 16, name: 'เสวนา/บรรยาย', icon: '🎙️' },

  // 🧘‍♂️ หมวดสุขภาพ
  { id: 17, name: 'สุขภาพ', icon: '🩺' },
  { id: 18, name: 'สุขภาพจิต', icon: '🧠' },
  { id: 19, name: 'กีฬา', icon: '⚽' },
  { id: 20, name: 'วิ่ง', icon: '🏃' },
  { id: 21, name: 'ฟิตเนส', icon: '💪' },
  { id: 22, name: 'เกษตร/ธรรมชาติ', icon: '🌱' },

  // 🎉 หมวดบันเทิง
  { id: 23, name: 'ดนตรี', icon: '🎵' },
  { id: 24, name: 'ภาพยนตร์', icon: '🍿' },
  { id: 25, name: 'ศิลปะ', icon: '🖌️' },
  { id: 26, name: 'ถ่ายภาพ', icon: '📷' },
  { id: 27, name: 'เกม', icon: '🎮' },
  { id: 28, name: 'บอร์ดเกม', icon: '🎲' },
  { id: 29, name: 'ท่องเที่ยว', icon: '✈️' },
  { id: 30, name: 'อาหาร', icon: '🍔' },
  { id: 31, name: 'แฟชั่น', icon: '👗' },
  { id: 32, name: 'สัตว์เลี้ยง', icon: '🐶' },
  { id: 33, name: 'มูเตลู', icon: '🔮' },

  // 🤝 หมวดกิจกรรม
  { id: 34, name: 'จิตอาสา', icon: '🤝' },
  { id: 35, name: 'ค่ายอาสา', icon: '⛺' },
  { id: 36, name: 'สิ่งแวดล้อม', icon: '♻️' },
  { id: 37, name: 'รับน้อง', icon: '🎉' },
  { id: 38, name: 'วัฒนธรรม', icon: '🙏' },
  { id: 39, name: 'เวิร์กชอป', icon: '🛠️' },
  { id: 40, name: 'การแข่งขัน', icon: '🥇' }
]

const filteredTags = computed(() => {
  if (!searchQuery.value) return tags.value
  const query = searchQuery.value.toLowerCase()
  return tags.value.filter(tag => 
    tag.name.toLowerCase().includes(query)
  )
})

const checkUserInterests = async () => {
  try {
    const token = localStorage.getItem('access')
    if (!token) {
      console.log('👤 User not logged in')
      return
    }

    const response = await tagService.checkUserHasInterests()
    if (!response.data.has_interests) {
      isOpen.value = true
      await fetchTags()
    }
  } catch (err) {
    console.error('❌ Error checking interests:', err)
  }
}

const fetchTags = async () => {
  loading.value = true
  try {
    const response = await tagService.getAllTags()
    if (response.data && response.data.length > 0) {
      tags.value = response.data
    } else {
      tags.value = MOCK_TAGS
    }
  } catch (err) {
    console.log('Using mock data')
    tags.value = MOCK_TAGS
  } finally {
    loading.value = false
  }
}

const toggleTag = (id) => {
  const index = selectedTags.value.indexOf(id)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(id)
  }
}

const submit = async () => {
  if (selectedTags.value.length === 0) return
  saving.value = true
  
  try {
    const tagsData = selectedTags.value.map(tagId => ({
      tag_id: tagId,
      score: 5.0
    }))

    await tagService.saveUserInterests(tagsData)
    
    isOpen.value = false
    window.location.reload()
    
  } catch (err) {
    console.error('❌ Error saving interests:', err)
    alert('เกิดข้อผิดพลาดในการบันทึก กรุณาลองใหม่อีกครั้ง')
  } finally {
    saving.value = false
  }
}

const skip = () => {
  isOpen.value = false
}

onMounted(() => {
  setTimeout(() => {
    checkUserInterests()
  }, 500)
})

if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => {
    if (e.key === 'access' && e.newValue) {
      checkUserInterests()
    }
  })
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #cbd5e1; }

@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes slide-up { from { opacity: 0; transform: translateY(30px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes fade-in-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes scale-in { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
@keyframes check-pop { 0% { transform: scale(0); } 80% { transform: scale(1.2); } 100% { transform: scale(1); } }

.animate-fade-in { animation: fade-in 0.3s ease-out; }
.animate-slide-up { animation: slide-up 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.animate-fade-in-up { animation: fade-in-up 0.6s ease-out 0.1s both; }
.animate-fade-in-up-delay { animation: fade-in-up 0.6s ease-out 0.2s both; }
.animate-scale-in { animation: scale-in 0.4s ease-out both; }
.animate-check-pop { animation: check-pop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
</style>