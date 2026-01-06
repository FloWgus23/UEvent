<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900">
    
    <header class="bg-blue-900/50 backdrop-blur-sm shadow-lg border-b border-blue-700">
      <div class="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
        <h1 class="text-white text-3xl font-bold">UEvent</h1>
        <div class="flex items-center gap-8">
          <router-link to="/organizer/dashboard" class="text-white text-lg hover:text-blue-200 transition">หน้าแรก</router-link>
          
          <div class="relative">
            <button @click="toggleDropdown" class="w-12 h-12 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition">
              <i class="fa-solid fa-user text-blue-900 text-xl"></i>
            </button>
            <div v-if="showDropdown" class="absolute right-0 mt-3 w-48 bg-white text-gray-800 rounded-lg shadow-xl py-2 z-50">
              <button class="w-full text-left px-4 py-3 text-red-600 hover:bg-red-50" @click="handleLogout">
                <i class="fa-solid fa-right-from-bracket mr-2"></i> ออกจากระบบ
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-4xl mx-auto px-8 py-12">
      <div class="bg-white rounded-3xl shadow-2xl p-10 animate-fade-up">
        <h2 class="text-3xl font-bold text-gray-800 mb-8">สร้างกิจกรรมใหม่</h2>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          
          <div>
            <label class="block text-gray-700 font-semibold mb-2">ชื่อกิจกรรม <span class="text-red-500">*</span></label>
            <input v-model="formData.name" type="text" placeholder="เช่น Hackathon 2025" class="w-full px-4 py-3 border-2 border-purple-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" required />
          </div>

          <div>
            <label class="block text-gray-700 font-semibold mb-2">รายละเอียด <span class="text-red-500">*</span></label>
            <textarea v-model="formData.description" rows="4" placeholder="รายละเอียดกิจกรรม..." class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none" required></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-gray-700 font-semibold mb-2">วันที่จัด <span class="text-red-500">*</span></label>
              <input v-model="formData.date" type="date" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2">เริ่มเวลา</label>
              <input v-model="formData.start_time" type="time" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2">สิ้นสุดเวลา</label>
              <input v-model="formData.end_time" type="time" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-gray-700 font-semibold mb-2">จำนวนรับ (คน) <span class="text-red-500">*</span></label>
              <input v-model="formData.capacity" type="number" min="1" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2">หมวดหมู่หลัก <span class="text-red-500">*</span></label>
              <div class="relative">
                <select v-model="formData.category" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg appearance-none bg-white cursor-pointer" required>
                  <option value="" disabled selected>-- เลือกหมวดหมู่ --</option>
                  <option value="academic">วิชาการและการเรียนรู้</option>
                  <option value="technology">เทคโนโลยีและนวัตกรรม</option>
                  <option value="entertainment">บันเทิงและนันทนาการ</option>
                  <option value="sports">กีฬาและสุขภาพ</option>
                  <option value="volunteer">จิตอาสาและสังคม</option>
                  <option value="career">แนะแนวและอาชีพ</option>
                  <option value="other">อื่นๆ</option>
                </select>
                <i class="fa-solid fa-chevron-down absolute right-4 top-3.5 text-gray-500 pointer-events-none"></i>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-gray-700 font-semibold mb-2">สถานที่ <span class="text-red-500">*</span></label>
              <input v-model="formData.location" type="text" placeholder="เช่น หอประชุมใหญ่" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
            </div>
            <div>
              <label class="block text-gray-700 font-semibold mb-2">ผู้จัด <span class="text-red-500">*</span></label>
              <input v-model="formData.organizer" type="text" placeholder="เช่น สโมสรนักศึกษา..." class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
            </div>
          </div>

          <div class="bg-gray-50 p-6 rounded-xl border border-gray-200">
            <div class="flex justify-between items-center mb-4">
              <label class="block text-gray-800 font-bold text-lg">
                แท็กที่เกี่ยวข้อง 
              </label>
              <span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold" v-if="selectedTagIds.length > 0">
                เลือกแล้ว {{ selectedTagIds.length }} รายการ
              </span>
            </div>
            
            <div v-if="availableTags.length === 0" class="text-center py-6 text-gray-400">
              <i class="fa-solid fa-circle-notch fa-spin"></i> กำลังโหลดข้อมูล...
            </div>
            
            <div v-else class="space-y-6 max-h-[400px] overflow-y-auto custom-scrollbar pr-2">
              
              <div v-for="(groupTags, groupName) in groupedTags" :key="groupName">
                <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 sticky top-0 bg-gray-50 py-1 z-10">
                  {{ groupName }}
                </h3>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="tag in groupTags"
                    :key="tag.id"
                    type="button"
                    @click="toggleTag(tag.id)"
                    class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 border flex items-center gap-2"
                    :class="selectedTagIds.includes(tag.id)
                      ? 'bg-blue-600 text-white border-blue-600 shadow-md transform scale-[1.02]'
                      : 'bg-white text-gray-600 border-gray-200 hover:border-blue-400 hover:text-blue-600'"
                  >
                    <span class="text-base">{{ tag.icon }}</span>
                    {{ tag.name }}
                    <i v-if="selectedTagIds.includes(tag.id)" class="fa-solid fa-check text-xs ml-1 bg-white/20 rounded-full p-0.5"></i>
                  </button>
                </div>
              </div>

            </div>
          </div>

          <div>
            <label class="block text-gray-700 font-semibold mb-2">รูปภาพปก</label>
            <div class="flex items-center gap-4 p-4 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-gray-100 transition">
              <label for="image" class="px-6 py-2 bg-white border border-gray-300 rounded-lg cursor-pointer hover:shadow-md transition text-gray-700 font-medium">
                <i class="fa-solid fa-cloud-arrow-up mr-2"></i> เลือกไฟล์
              </label>
              <input id="image" type="file" @change="handleImageUpload" accept="image/*" class="hidden" />
              <span class="text-gray-500 text-sm truncate max-w-xs">{{ imageFileName || 'ยังไม่ได้เลือกไฟล์' }}</span>
            </div>
          </div>

          <div class="flex gap-4 pt-6">
            <button type="submit" :disabled="isLoading" class="flex-1 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-bold text-lg shadow-lg transition transform hover:scale-[1.02] disabled:opacity-50">
              <span v-if="isLoading"><i class="fa-solid fa-circle-notch fa-spin mr-2"></i> กำลังบันทึก...</span>
              <span v-else>+ สร้างกิจกรรม</span>
            </button>
            <button type="button" @click="handleCancel" :disabled="isLoading" class="px-8 py-4 bg-white border-2 border-gray-200 text-gray-600 hover:text-red-600 hover:border-red-200 rounded-xl font-semibold transition">
              ยกเลิก
            </button>
          </div>

        </form>
      </div>
    </div>

    <footer class="bg-blue-900/50 backdrop-blur-sm text-white py-6 mt-12 text-center">
      <p class="text-sm opacity-80">© 2025 UEvent Organizer System</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import activityService from '@/services/activityService.js'
import tagService from '@/services/tagService.js'

const router = useRouter()
const showDropdown = ref(false)
const isLoading = ref(false)

// Data
const availableTags = ref([]) 
const selectedTagIds = ref([]) 
const imageFile = ref(null)
const imageFileName = ref('')

const formData = ref({
  name: '', description: '', date: '', start_time: '', end_time: '',
  capacity: '', location: '', organizer: '', category: ''
})

// ⭐ รายชื่อแท็กสำรอง (ใช้แสดงผลถ้า API ยังไม่พร้อม)
const FALLBACK_TAGS = [
  // 🎓 วิชาการ
  { id: 1, name: 'Coding', icon: '💻' }, { id: 2, name: 'AI & Data', icon: '🤖' },
  { id: 3, name: 'Innovation', icon: '💡' }, { id: 4, name: 'Science', icon: '🔬' },
  { id: 5, name: 'Design', icon: '🎨' }, { id: 6, name: 'Media', icon: '🎬' },
  { id: 7, name: 'Language', icon: '🗣️' }, { id: 8, name: 'Tutoring', icon: '📚' },
  // 💼 อาชีพ
  { id: 9, name: 'Business', icon: '💼' }, { id: 10, name: 'Marketing', icon: '📈' },
  { id: 11, name: 'Finance', icon: '💰' }, { id: 12, name: 'Startup', icon: '🚀' },
  { id: 13, name: 'Career', icon: '👔' }, { id: 14, name: 'Law & Politics', icon: '⚖️' },
  { id: 15, name: 'Leadership', icon: '🏆' }, { id: 16, name: 'Talk', icon: '🎙️' },
  // 🧘‍♂️ สุขภาพ
  { id: 17, name: 'Health', icon: '🩺' }, { id: 18, name: 'Mental Health', icon: '🧠' },
  { id: 19, name: 'Sports', icon: '⚽' }, { id: 20, name: 'Running', icon: '🏃' },
  { id: 21, name: 'Fitness', icon: '💪' }, { id: 22, name: 'Agriculture', icon: '🌱' },
  // 🎉 บันเทิง
  { id: 23, name: 'Music', icon: '🎵' }, { id: 24, name: 'Movie', icon: '🍿' },
  { id: 25, name: 'Art', icon: '🖌️' }, { id: 26, name: 'Photography', icon: '📷' },
  { id: 27, name: 'Game', icon: '🎮' }, { id: 28, name: 'Board Game', icon: '🎲' },
  { id: 29, name: 'Travel', icon: '✈️' }, { id: 30, name: 'Food', icon: '🍔' },
  { id: 31, name: 'Fashion', icon: '👗' }, { id: 32, name: 'Pets', icon: '🐶' },
  { id: 33, name: 'Mootelu', icon: '🔮' },
  // 🤝 สังคม
  { id: 34, name: 'Volunteer', icon: '🤝' }, { id: 35, name: 'Rural Camp', icon: '⛺' },
  { id: 36, name: 'Environment', icon: '♻️' }, { id: 37, name: 'Freshy', icon: '🎉' },
  { id: 38, name: 'Culture', icon: '🙏' }, { id: 39, name: 'Workshop', icon: '🛠️' },
  { id: 40, name: 'Competition', icon: '🥇' }
]

// ⭐ Computed Property สำหรับจัดกลุ่มแท็ก
const groupedTags = computed(() => {
  const groups = {
    '🎓 วิชาการ & ทักษะ': ['Coding', 'AI & Data', 'Innovation', 'Science', 'Design', 'Media', 'Language', 'Tutoring'],
    '💼 ธุรกิจ & สังคม': ['Business', 'Marketing', 'Finance', 'Startup', 'Career', 'Law & Politics', 'Leadership', 'Talk'],
    '🧘‍♂️ สุขภาพ & กีฬา': ['Health', 'Mental Health', 'Sports', 'Running', 'Fitness', 'Agriculture'],
    '🎉 บันเทิง & ไลฟ์สไตล์': ['Music', 'Movie', 'Art', 'Photography', 'Game', 'Board Game', 'Travel', 'Food', 'Fashion', 'Pets', 'Mootelu'],
    '🤝 กิจกรรม & จิตอาสา': ['Volunteer', 'Rural Camp', 'Environment', 'Freshy', 'Culture', 'Workshop', 'Competition']
  }

  const result = {}
  
  // สร้างถังเก็บตามกลุ่ม
  Object.keys(groups).forEach(key => result[key] = [])
  result['📌 อื่นๆ'] = []

  // วนลูปแท็กทั้งหมดแล้วหยอดลงถัง
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

  // ลบถังเปล่าออก
  return Object.fromEntries(Object.entries(result).filter(([_, tags]) => tags.length > 0))
})

const toggleDropdown = () => { showDropdown.value = !showDropdown.value }
const closeDropdown = () => { showDropdown.value = false }
const handleLogout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('isAdmin')
  closeDropdown()
  router.push('/')
}

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

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
    imageFileName.value = file.name
  }
}

const handleSubmit = async () => {
  try {
    if (!formData.value.category) return alert('กรุณาเลือกหมวดหมู่กิจกรรม')
    if (formData.value.start_time && formData.value.end_time) {
      if (formData.value.end_time <= formData.value.start_time) return alert('เวลาสิ้นสุดต้องมากกว่าเวลาเริ่มต้น')
    }

    isLoading.value = true
    const submitData = new FormData()
    
    Object.keys(formData.value).forEach(key => submitData.append(key, formData.value[key]))
    selectedTagIds.value.forEach(id => submitData.append('tag_ids', id))
    if (imageFile.value) submitData.append('image', imageFile.value)

    await activityService.createActivity(submitData)
    alert('✅ สร้างกิจกรรมสำเร็จเรียบร้อย!')
    router.push('/organizer/dashboard')

  } catch (error) {
    console.error('Error:', error)
    alert('❌ เกิดข้อผิดพลาด กรุณาลองใหม่')
  } finally {
    isLoading.value = false
  }
}

const handleCancel = () => {
  if (confirm('ต้องการยกเลิกหรือไม่?')) router.push('/organizer/dashboard')
}

onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.animate-fade-up { animation: fadeUp 0.5s ease-out; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>