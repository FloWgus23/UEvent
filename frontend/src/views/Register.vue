<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center px-4 py-8 relative overflow-hidden">
    
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
      <div class="absolute top-[-10%] right-[-5%] w-96 h-96 bg-blue-500/20 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-[-10%] left-[-5%] w-72 h-72 bg-purple-500/20 rounded-full blur-[80px]"></div>
    </div>

    <button 
      @click="$router.push('/')" 
      class="fixed top-6 left-6 z-50 flex items-center gap-3 px-2 py-2 pr-5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20 transition-all duration-300 group shadow-lg hover:shadow-blue-500/20"
    >
      <div class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center group-hover:bg-white/20 transition-all border border-white/10">
        <i class="fa-solid fa-arrow-left text-sm group-hover:-translate-x-1 transition-transform"></i>
      </div>
      <span class="font-medium tracking-wide text-sm text-white/90 group-hover:text-white">กลับหน้าแรก</span>
    </button>

    <div class="w-full max-w-2xl relative z-10">
      <div class="bg-white rounded-3xl shadow-2xl p-8 md:p-12 animate-fade-in-up">
        
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-50 text-blue-600 mb-4">
            <i class="fa-solid fa-user-plus text-2xl"></i>
          </div>
          <h1 class="text-gray-800 text-3xl md:text-4xl font-bold mb-2 tracking-tight">
            สร้างบัญชีใหม่
          </h1>
          <p class="text-gray-500 text-sm">กรอกข้อมูลเพื่อเริ่มต้นใช้งาน UEvent</p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-5">
          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
              ชื่อ - สกุล <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.fullname"
              type="text"
              required
              class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all placeholder-gray-400"
              placeholder="กรอกชื่อและนามสกุลจริง"
            />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
                Username <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formData.username"
                type="text"
                required
                class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all placeholder-gray-400"
                placeholder="ภาษาอังกฤษเท่านั้น"
              />
            </div>
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
                อีเมล <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formData.email"
                type="email"
                required
                class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all placeholder-gray-400"
                placeholder="name@example.com"
              />
            </div>
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
              เบอร์โทรศัพท์ <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.phone"
              type="tel"
              required
              class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all placeholder-gray-400"
              placeholder="0812345678"
            />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
                เพศ <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <select
                  v-model="formData.gender"
                  required
                  class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all appearance-none cursor-pointer"
                >
                  <option value="" disabled>เลือกเพศ</option>
                  <option value="male">ชาย</option>
                  <option value="female">หญิง</option>
                  <option value="other">อื่นๆ</option>
                </select>
                <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
                  <i class="fa-solid fa-chevron-down text-xs"></i>
                </div>
              </div>
            </div>

            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
                คณะ <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <select
                  v-model="formData.faculty"
                  required
                  class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all appearance-none cursor-pointer"
                >
                  <option value="" disabled>เลือกคณะ</option>
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
                <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
                  <i class="fa-solid fa-chevron-down text-xs"></i>
                </div>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
              วันเกิด <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-3 gap-3">
              <div class="relative">
                <select v-model="formData.birthDay" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all appearance-none">
                  <option value="" disabled>วัน</option>
                  <option v-for="d in 31" :key="d" :value="d">{{ d }}</option>
                </select>
                <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400 text-xs"><i class="fa-solid fa-chevron-down"></i></div>
              </div>
              
              <div class="relative">
                <select v-model="formData.birthMonth" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all appearance-none">
                  <option value="" disabled>เดือน</option>
                  <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
                </select>
                <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400 text-xs"><i class="fa-solid fa-chevron-down"></i></div>
              </div>

              <div class="relative">
                <select v-model="formData.birthYear" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all appearance-none">
                  <option value="" disabled>ปี พ.ศ.</option>
                  <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>
                <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400 text-xs"><i class="fa-solid fa-chevron-down"></i></div>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
              รหัสผ่าน <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.password"
              type="password"
              required
              class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all placeholder-gray-400"
              placeholder="••••••••"
            />
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2 pl-1">
              ยืนยันรหัสผ่าน <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.confirmPassword"
              type="password"
              required
              class="w-full px-5 py-3 rounded-xl border-2 border-gray-100 bg-gray-50 text-gray-800 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all placeholder-gray-400"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-500/30 transition-all transform active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg mt-6"
          >
            <i v-if="isLoading" class="fa-solid fa-circle-notch fa-spin"></i>
            <span>{{ isLoading ? 'กำลังลงทะเบียน...' : 'สมัครสมาชิก' }}</span>
          </button>
        </form>

        <div class="mt-8 text-center">
          <p class="text-gray-500 text-sm">
            มีบัญชีอยู่แล้ว? 
            <router-link to="/login" class="text-blue-600 font-bold hover:text-blue-800 transition-colors ml-1">
              เข้าสู่ระบบเลย
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
// import axios from 'axios'  <-- เอาออก
import api from '../services/api' // <-- ✅ เปลี่ยนมาใช้ตัวนี้แทน (ตรวจสอบว่าไฟล์ api.js อยู่ที่ src/services/api.js นะครับ)

const router = useRouter()
const isLoading = ref(false)

const months = [
  'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
  'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
]

const currentYear = new Date().getFullYear() + 543
const years = computed(() => {
  const y = []
  for (let i = currentYear; i >= currentYear - 100; i--) {
    y.push(i)
  }
  return y
})

const formData = ref({
  fullname: '',
  username: '',
  email: '',
  phone: '',
  gender: '',
  faculty: '',
  birthDay: '',
  birthMonth: '',
  birthYear: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (formData.value.password !== formData.value.confirmPassword) {
    alert('รหัสผ่านไม่ตรงกัน')
    return
  }
  if (formData.value.password.length < 6) {
    alert('รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร')
    return
  }
  if (!formData.value.birthDay || !formData.value.birthMonth || !formData.value.birthYear) {
    alert('กรุณาระบุวันเกิดให้ครบถ้วน')
    return
  }

  try {
    isLoading.value = true

    // แยกชื่อ-นามสกุล
    const fullNameString = formData.value.fullname.trim()
    const nameParts = fullNameString.split(' ')
    const firstName = nameParts[0]
    const lastName = nameParts.slice(1).join(' ')

    // Format วันเกิด
    const year = parseInt(formData.value.birthYear) - 543
    const month = String(formData.value.birthMonth).padStart(2, '0')
    const day = String(formData.value.birthDay).padStart(2, '0')
    const birthDateString = `${year}-${month}-${day}`

    const registerData = {
      username: formData.value.username,
      email: formData.value.email,
      password: formData.value.password,
      first_name: firstName,
      last_name: lastName,
      profile: {
          phone: formData.value.phone,
          gender: formData.value.gender,
          faculty: formData.value.faculty,
          birthdate: birthDateString
      }
    }

    console.log('Sending Register data:', registerData)

    // ✅ เปลี่ยนเป็น api.post และตัด URL ยาวๆ ออก เหลือแค่ path
    const response = await api.post('/auth/register/', registerData)
    
    console.log('Registration Success:', response.data)
    alert('ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ')
    router.push('/login')

  } catch (error) {
    console.error('Registration error:', error)
    const msg = error.response?.data?.message || error.response?.data?.error || 'เกิดข้อผิดพลาดในการลงทะเบียน'
    if (typeof error.response?.data === 'object') {
       alert('เกิดข้อผิดพลาด: ' + JSON.stringify(error.response.data))
    } else {
       alert(msg)
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>