<template>
  <div class="min-h-screen bg-gray-50">
    
    <nav class="bg-[#1E3A8A] border-b border-blue-400">
      <div class="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center text-white">
        <router-link to="/" class="text-3xl font-bold">UEvent</router-link>
        <router-link to="/" class="hover:text-blue-200">กลับหน้าหลัก</router-link>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto py-12 px-6">
      
      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-900 mx-auto"></div>
        <p class="mt-4 text-gray-500">กำลังโหลดข้อมูลโปรไฟล์...</p>
      </div>

      <div v-else class="bg-white rounded-3xl shadow-xl overflow-hidden animate-fade-up">
        
        <div class="h-40 bg-gradient-to-r from-blue-800 to-blue-600 relative">
          <div class="absolute inset-0 bg-black/10"></div>
        </div>

        <div class="px-8 pb-8 relative">
          
          <!-- Profile Image Section -->
          <div class="-mt-16 mb-6 flex justify-between items-end">
            <div class="relative group">
              <div class="w-32 h-32 bg-white rounded-full p-2 shadow-lg">
                <div class="w-full h-full bg-gray-100 rounded-full flex items-center justify-center text-5xl text-gray-400 overflow-hidden relative">
                  <img 
                    v-if="user.profile?.profile_image" 
                    :src="user.profile.profile_image" 
                    alt="Profile" 
                    class="w-full h-full object-cover"
                  />
                  <i v-else class="fa-solid fa-user"></i>
                  
                  <!-- Upload Overlay -->
                  <label class="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                    <i class="fa-solid fa-camera text-white text-2xl"></i>
                    <input 
                      type="file" 
                      @change="handleImageUpload" 
                      accept="image/*" 
                      class="hidden"
                    />
                  </label>
                </div>
              </div>
              
              <!-- Delete Image Button -->
              <button 
                v-if="user.profile?.profile_image"
                @click="handleDeleteImage"
                class="absolute -bottom-1 -right-1 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg flex items-center justify-center transition"
                title="ลบรูปโปรไฟล์"
              >
                <i class="fa-solid fa-trash text-xs"></i>
              </button>
            </div>

            <button 
              @click="showEditModal = true"
              class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition text-sm"
            >
              <i class="fa-solid fa-pen-to-square mr-2"></i> แก้ไขข้อมูล
            </button>
          </div>

          <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">
              {{ getDisplayName() }}
            </h1>
            <p class="text-gray-500 flex items-center gap-2 mt-1">
              <i class="fa-regular fa-envelope"></i> {{ user.email || '-' }}
            </p>
            
            <div class="mt-3 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium" 
                 :class="user.is_superuser ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'">
              <i :class="user.is_superuser ? 'fa-solid fa-shield-halved mr-2' : 'fa-solid fa-user mr-2'"></i>
              {{ user.is_superuser ? 'ผู้ดูแลระบบ (Admin)' : 'สมาชิกทั่วไป (User)' }}
            </div>
          </div>

          <hr class="border-gray-100 my-8">

          <h2 class="text-xl font-bold text-gray-800 mb-6">ข้อมูลส่วนตัว</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-y-6 gap-x-12">
            
            <div class="space-y-1">
              <label class="text-sm text-gray-500">ชื่อผู้ใช้งาน (Username)</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                {{ user.username || '-' }}
              </div>
            </div>

            <div class="space-y-1">
              <label class="text-sm text-gray-500">อีเมล</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                {{ user.email || '-' }}
              </div>
            </div>

            <div class="space-y-1">
              <label class="text-sm text-gray-500">ชื่อจริง</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                {{ user.first_name || '-' }}
              </div>
            </div>

            <div class="space-y-1">
              <label class="text-sm text-gray-500">นามสกุล</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                {{ user.last_name || '-' }}
              </div>
            </div>

            <div class="space-y-1">
              <label class="text-sm text-gray-500">เบอร์โทรศัพท์</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                {{ user.profile?.phone || '-' }}
              </div>
            </div>

            <div class="space-y-1">
              <label class="text-sm text-gray-500">วันที่สมัครสมาชิก</label>
              <div class="font-medium text-gray-900">
                <i class="fa-regular fa-calendar-days mr-2 text-blue-500"></i>
                {{ user.date_joined || '-' }}
              </div>
            </div>

            <!-- ⭐ เพิ่มส่วนนี้: แสดง เพศ -->
            <div class="space-y-1">
              <label class="text-sm text-gray-500">เพศ</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                {{ getGenderDisplay(user.profile?.gender) }}
              </div>
            </div>

            <!-- ⭐ เพิ่มส่วนนี้: แสดง คณะ -->
            <div class="space-y-1">
              <label class="text-sm text-gray-500">คณะ</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                {{ getFacultyDisplay(user.profile?.faculty) }}
              </div>
            </div>

            <!-- ⭐ เพิ่มส่วนนี้: แสดง วันเกิด -->
            <div class="space-y-1">
              <label class="text-sm text-gray-500">วันเกิด</label>
              <div class="font-medium text-gray-900 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100">
                <i class="fa-solid fa-cake-candles mr-2 text-pink-500"></i>
                {{ formatBirthdate(user.profile?.birthdate) }}
              </div>
            </div>

          </div>


        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showEditModal = false"></div>

      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden animate-fade-up">
        
        <div class="bg-blue-900 px-6 py-4 flex justify-between items-center">
          <h3 class="text-xl font-bold text-white">แก้ไขข้อมูลโปรไฟล์</h3>
          <button @click="showEditModal = false" class="text-blue-200 hover:text-white text-2xl font-bold">&times;</button>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">ชื่อจริง</label>
              <input 
                v-model="editForm.first_name" 
                type="text" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="กรอกชื่อจริง"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">นามสกุล</label>
              <input 
                v-model="editForm.last_name" 
                type="text" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="กรอกนามสกุล"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">อีเมล</label>
              <input 
                v-model="editForm.email" 
                type="email" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="กรอกอีเมล"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">เบอร์โทรศัพท์</label>
              <input 
                v-model="editForm.phone" 
                type="tel" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="กรอกเบอร์โทรศัพท์"
              >
            </div>

            <!-- ⭐ เพิ่มส่วนนี้: เพศ -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">เพศ</label>
              <select 
                v-model="editForm.gender" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="">เลือกเพศ</option>
                <option value="male">ชาย</option>
                <option value="female">หญิง</option>
                <option value="other">อื่นๆ</option>
              </select>
            </div>

            <!-- ⭐ เพิ่มส่วนนี้: คณะ -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">คณะ</label>
              <select 
                v-model="editForm.faculty" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="">เลือกคณะ</option>
                <option value="science">คณะวิทยาศาสตร์</option>
                <option value="engineering">คณะวิศวกรรมศาสตร์</option>
                <option value="business">คณะบริหารศาสตร์</option>
                <option value="liberal_arts">คณะศิลปศาสตร์</option>
                <option value="agriculture">คณะเกษตรศาสตร์</option>
                <option value="nursing">คณะพยาบาลศาสตร์</option>
                <option value="pharmacy">คณะเภสัชศาสตร์</option>
                <option value="law">คณะนิติศาสตร์</option>
                <option value="political">คณะรัฐศาสตร์</option>
                <option value="other">อื่นๆ</option>
              </select>
            </div>

            <!-- ⭐ เพิ่มส่วนนี้: วันเกิด -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">วันเกิด</label>
              <input 
                v-model="editForm.birthdate" 
                type="date" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
            </div>

          </div>
        </div>

        <div class="px-6 py-4 bg-gray-50 flex gap-3 justify-end border-t border-gray-100">
          <button 
            @click="showEditModal = false"
            class="px-5 py-2 text-gray-600 hover:bg-gray-200 rounded-lg transition font-medium"
          >
            ยกเลิก
          </button>
          <button 
            @click="handleUpdateProfile"
            :disabled="isSubmitting"
            class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold shadow-md transition disabled:opacity-50 flex items-center gap-2"
          >
            <span v-if="isSubmitting" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ isSubmitting ? 'กำลังบันทึก...' : 'บันทึกข้อมูล' }}
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'
import apiClient from '@/services/api'

const router = useRouter()
const user = ref({})
const isLoading = ref(true)
const showEditModal = ref(false)
const isSubmitting = ref(false)

const editForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  gender: '',
  faculty: '',
  birthdate: ''
})

const fetchUserProfile = async () => {
  try {
    const res = await authService.getUserProfile()
    user.value = res.data
    
    console.log('User data:', user.value) // ⭐ Debug ดูข้อมูลที่ได้
    
    // Set edit form
    editForm.value = {
      first_name: user.value.first_name || '',
      last_name: user.value.last_name || '',
      email: user.value.email || '',
      phone: user.value.profile?.phone || '',
      gender: user.value.profile?.gender || '',
      faculty: user.value.profile?.faculty || '',
      birthdate: user.value.profile?.birthdate || ''
    }
  } catch (err) {
    console.error(err)
    if (err.response && err.response.status === 401) {
      alert('Session หมดอายุ กรุณาเข้าสู่ระบบใหม่')
      localStorage.removeItem('access')
      router.push('/login')
    }
  } finally {
    isLoading.value = false
  }
}

// ⭐ ฟังก์ชันแสดงชื่อ
const getDisplayName = () => {
  // ถ้ามี fullname จาก API ใหม่
  if (user.value.fullname) {
    return user.value.fullname
  }
  
  // ถ้ามี first_name + last_name
  if (user.value.first_name && user.value.last_name) {
    return `${user.value.first_name} ${user.value.last_name}`
  }
  
  // ถ้ามีแค่ first_name
  if (user.value.first_name) {
    return user.value.first_name
  }
  
  // ถ้าไม่มีอะไรเลย ให้ใช้ username
  return user.value.username || 'ไม่ระบุชื่อ'
}

// ⭐ ฟังก์ชันแปลงเพศ
const getGenderDisplay = (gender) => {
  const genderMap = {
    'male': 'ชาย',
    'female': 'หญิง',
    'other': 'อื่นๆ'
  }
  return genderMap[gender] || '-'
}

// ⭐ ฟังก์ชันแปลงคณะ
const getFacultyDisplay = (faculty) => {
  const facultyMap = {
    'science': 'คณะวิทยาศาสตร์',
    'engineering': 'คณะวิศวกรรมศาสตร์',
    'business': 'คณะบริหารศาสตร์',
    'liberal_arts': 'คณะศิลปศาสตร์',
    'agriculture': 'คณะเกษตรศาสตร์',
    'nursing': 'คณะพยาบาลศาสตร์',
    'pharmacy': 'คณะเภสัชศาสตร์',
    'law': 'คณะนิติศาสตร์',
    'political': 'คณะรัฐศาสตร์',
    'other': 'อื่นๆ'
  }
  return facultyMap[faculty] || '-'
}

// ⭐ ฟังก์ชันแปลงวันเกิด
const formatBirthdate = (birthdate) => {
  if (!birthdate) return '-'
  
  try {
    const date = new Date(birthdate)
    return date.toLocaleDateString('th-TH', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return birthdate
  }
}

// ⭐ อัปโหลดรูปโปรไฟล์
const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // ตรวจสอบประเภทไฟล์
  if (!file.type.startsWith('image/')) {
    alert('กรุณาเลือกไฟล์รูปภาพเท่านั้น')
    return
  }

  // ตรวจสอบขนาดไฟล์ (ไม่เกิน 5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('ขนาดไฟล์ต้องไม่เกิน 5MB')
    return
  }

  try {
    const formData = new FormData()
    formData.append('profile_image', file)

    const res = await apiClient.post('/auth/me/upload-image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    user.value = res.data.data
    alert('✅ อัปโหลดรูปโปรไฟล์สำเร็จ')
  } catch (err) {
    console.error(err)
    alert('❌ ไม่สามารถอัปโหลดรูปภาพได้')
  }
}

// ⭐ ลบรูปโปรไฟล์
const handleDeleteImage = async () => {
  if (!confirm('คุณต้องการลบรูปโปรไฟล์หรือไม่?')) return

  try {
    const res = await apiClient.delete('/auth/me/delete-image/')
    user.value = res.data.data
    alert('✅ ลบรูปโปรไฟล์สำเร็จ')
  } catch (err) {
    console.error(err)
    alert('❌ ไม่สามารถลบรูปภาพได้')
  }
}

// ⭐ อัปเดตข้อมูลโปรไฟล์
const handleUpdateProfile = async () => {
  try {
    isSubmitting.value = true

    const res = await apiClient.patch('/auth/me/', editForm.value)
    user.value = res.data.data
    
    alert('✅ อัปเดตข้อมูลสำเร็จ')
    showEditModal.value = false
  } catch (err) {
    console.error(err)
    alert('❌ ไม่สามารถอัปเดตข้อมูลได้')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchUserProfile()
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-up {
  animation: fadeUp 0.5s ease-out;
}
</style>