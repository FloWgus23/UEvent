<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center px-4 py-8 relative overflow-hidden font-sans">
    
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
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-50 text-blue-600 mb-4 shadow-sm">
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
import axios from 'axios'
import Swal from 'sweetalert2'

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

// --- ฟังก์ชันช่วยแสดง Alert แบบสวยงาม ---
const showToast = (icon, title, text) => {
  Swal.fire({
    icon: icon,
    title: title,
    text: text,
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })
}

// Helper function for validation errors (Prettier)
const showValidationError = (title, text) => {
    Swal.fire({
        html: `
            <div class="mt-2 mb-4">
                <i class="fa-solid fa-triangle-exclamation text-5xl text-amber-500"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2 font-sans">${title}</h3>
            <p class="text-gray-600 text-sm font-sans">${text}</p>
        `,
        showConfirmButton: true,
        confirmButtonText: 'ตกลง',
        buttonsStyling: false,
        customClass: {
            popup: 'rounded-3xl shadow-xl border border-amber-100 font-sans p-6',
            confirmButton: 'bg-amber-500 hover:bg-amber-600 text-white px-6 py-2.5 rounded-xl font-semibold transition-all shadow-md hover:shadow-lg focus:outline-none focus:ring-4 focus:ring-amber-500/20 active:scale-95'
        }
    })
}

const handleRegister = async () => {
  // Validation Alerts (สวยขึ้น)
  if (formData.value.password !== formData.value.confirmPassword) {
    showValidationError('รหัสผ่านไม่ตรงกัน', 'กรุณาตรวจสอบรหัสผ่านอีกครั้ง')
    return
  }
  if (formData.value.password.length < 6) {
    showValidationError('รหัสผ่านสั้นเกินไป', 'รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร')
    return
  }
  if (!formData.value.birthDay || !formData.value.birthMonth || !formData.value.birthYear) {
    showValidationError('ข้อมูลไม่ครบถ้วน', 'กรุณาระบุวันเกิดให้ครบถ้วน')
    return
  }

  try {
    isLoading.value = true

    // Prepare data
    const fullNameString = formData.value.fullname.trim()
    const nameParts = fullNameString.split(' ') 
    const firstName = nameParts[0]
    const lastName = nameParts.slice(1).join(' ') 

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

    await axios.post('http://127.0.0.1:8000/api/auth/register/', registerData)
    
    // ⭐⭐⭐ Alert สำเร็จแบบสวยงาม (Premium Look) ⭐⭐⭐
    await Swal.fire({
      // ไม่ใช้ icon มาตรฐาน แต่ใช้ HTML เพื่อใส่ Font Awesome แทน
      html: `
        <div class="mt-4 mb-6">
            <i class="fa-solid fa-circle-check text-7xl text-blue-500 animate-bounce-once"></i>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2 font-sans">ลงทะเบียนสำเร็จ!</h2>
        <p class="text-gray-600 font-sans">ยินดีต้อนรับสู่ UEvent<br>กำลังนำคุณไปยังหน้าเข้าสู่ระบบ...</p>
      `,
      showConfirmButton: false, // ไม่ต้องมีปุ่มกด
      timer: 2500, // รอ 2.5 วินาที
      timerProgressBar: true,
      // ปรับแต่ง CSS ของ Popup และ Progress Bar
      customClass: {
        popup: 'rounded-[2rem] shadow-2xl border border-blue-50 font-sans pb-8',
        timerProgressBar: 'bg-blue-500 h-1.5' // แถบสีน้ำเงิน
      },
      willClose: () => {
        router.push('/login')
      }
    })

  } catch (error) {
    console.error('Registration error:', error)
    const msg = error.response?.data?.message || error.response?.data?.error || 'เกิดข้อผิดพลาดในการลงทะเบียน'
    
    // Alert Error แบบสวยงาม (Premium Look)
    Swal.fire({
        html: `
            <div class="mt-4 mb-4">
                <i class="fa-solid fa-circle-xmark text-6xl text-red-500"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2 font-sans">เกิดข้อผิดพลาด</h3>
            <p class="text-red-600 text-sm font-sans px-4">${typeof error.response?.data === 'object' ? JSON.stringify(error.response.data) : msg}</p>
        `,
        showConfirmButton: true,
        confirmButtonText: 'ลองใหม่อีกครั้ง',
        buttonsStyling: false,
        customClass: {
            popup: 'rounded-3xl shadow-xl border border-red-50 font-sans p-6',
            confirmButton: 'bg-red-500 hover:bg-red-600 text-white px-6 py-2.5 rounded-xl font-semibold transition-all shadow-md hover:shadow-lg focus:outline-none focus:ring-4 focus:ring-red-500/20 mt-4 active:scale-95'
        }
    })

  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* กำหนด Font หลักให้ SweetAlert2 ผ่าน class นี้ */
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

/* Animation สำหรับไอคอนใน Alert */
.animate-bounce-once {
    animation: bounce-once 1s;
}

@keyframes bounce-once {
  0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
  40% {transform: translateY(-20px);}
  60% {transform: translateY(-10px);}
}

/* Override SweetAlert2 Default Styles (Optional but recommended for cleaner look) */
:deep(.swal2-popup) {
    padding-top: 1.5rem !important;
}
:deep(.swal2-html-container) {
    margin: 0 !important;
    overflow: visible !important;
}
</style>