<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F] flex flex-col">
    
    <nav class="fixed top-0 w-full z-50 bg-gradient-to-r from-[#0F172A] via-[#1E3A8A] to-[#1E40AF] text-white shadow-lg border-b border-white/10 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          
          <router-link to="/" class="text-2xl font-bold tracking-tight flex items-center gap-2 hover:opacity-90 transition-opacity">
            <i class="fa-solid fa-calendar-star text-white text-2xl drop-shadow-md"></i>
            <span class="font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-100">UEvent</span>
          </router-link>

          <div class="flex items-center gap-8">
            <div class="hidden md:flex items-center gap-6 text-[15px] font-medium text-blue-100">
              <router-link to="/" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all">หน้าแรก</router-link>
              <router-link to="/category" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all">หมวดหมู่</router-link>
              <router-link to="/news" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all">ข่าวสาร</router-link>
            </div>

            <button
              @click="showMobileMenu = !showMobileMenu"
              class="md:hidden text-white p-2 rounded-lg hover:bg-white/10 transition-colors"
              aria-label="เปิดเมนู"
            >
              <i :class="showMobileMenu ? 'fa-solid fa-xmark' : 'fa-solid fa-bars'" class="text-xl"></i>
            </button>

            <router-link to="/register" class="bg-white text-blue-900 hover:bg-blue-50 px-5 py-2 rounded-full text-sm font-bold transition-all shadow-lg hover:shadow-xl transform active:scale-95">
              ลงทะเบียน
            </router-link>
          </div>
        </div>
      </div>

      <div
        v-if="showMobileMenu"
        class="md:hidden bg-[#1E3A8A]/95 backdrop-blur-xl border-t border-white/10 animate-fade-in-down"
      >
        <div class="px-6 py-4 flex flex-col gap-2">
          <router-link to="/" @click="showMobileMenu = false" class="px-4 py-3 rounded-lg text-blue-100 hover:bg-white/10 hover:text-white font-medium">หน้าแรก</router-link>
          <router-link to="/category" @click="showMobileMenu = false" class="px-4 py-3 rounded-lg text-blue-100 hover:bg-white/10 hover:text-white font-medium">หมวดหมู่</router-link>
          <router-link to="/news" @click="showMobileMenu = false" class="px-4 py-3 rounded-lg text-blue-100 hover:bg-white/10 hover:text-white font-medium">ข่าวสาร</router-link>
        </div>
      </div>
    </nav>

    <div class="flex-grow flex items-center justify-center px-6 pt-24 pb-12 relative overflow-hidden">
      
      <div class="absolute top-0 left-1/4 w-[600px] h-[600px] bg-blue-200/40 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>
      <div class="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-indigo-200/40 rounded-full blur-[100px] pointer-events-none"></div>

      <div class="bg-white rounded-[2rem] shadow-2xl w-full max-w-md p-8 md:p-10 relative z-10 animate-fade-up border border-white/50">
        
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4 shadow-sm">
             <i class="fa-solid fa-right-to-bracket"></i>
          </div>
          <h2 class="text-3xl font-bold text-gray-900 tracking-tight">เข้าสู่ระบบ</h2>
          <p class="text-gray-500 text-sm mt-2">ยินดีต้อนรับกลับสู่ UEvent</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div class="space-y-1">
            <label for="username" class="text-xs font-bold text-gray-500 uppercase tracking-wider ml-1">ชื่อผู้ใช้</label>
            <div class="relative">
              <i class="fa-regular fa-user absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
              <input
                id="username"
                v-model="username"
                type="text"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-gray-800 font-medium"
                placeholder="ระบุชื่อผู้ใช้"
                required
              />
            </div>
          </div>

          <div class="space-y-1">
            <div class="flex justify-between items-center ml-1">
              <label for="password" class="text-xs font-bold text-gray-500 uppercase tracking-wider">รหัสผ่าน</label>
              <router-link to="/forgot-password" class="text-xs font-bold text-blue-600 hover:text-blue-700 hover:underline">
                ลืมรหัสผ่าน?
              </router-link>
            </div>
            
             <div class="relative">
              <i class="fa-solid fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
              <input
                id="password"
                v-model="password"
                type="password"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-gray-800 font-medium"
                placeholder="ระบุรหัสผ่าน"
                required
              />
            </div>
          </div>

          <div v-if="error" class="bg-red-50 text-red-600 text-sm px-4 py-3 rounded-xl flex items-center gap-2 animate-shake border border-red-100">
            <i class="fa-solid fa-circle-exclamation"></i>
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-blue-200 transition-all transform hover:-translate-y-0.5 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-2 mt-4"
          >
            <i v-if="isLoading" class="fa-solid fa-circle-notch fa-spin"></i>
            <span>{{ isLoading ? 'กำลังตรวจสอบ...' : 'เข้าสู่ระบบ' }}</span>
          </button>
        </form>

        <div class="text-center mt-6 text-sm text-gray-500">
          ยังไม่มีบัญชีผู้ใช้? 
          <router-link to="/register" class="text-blue-600 font-bold hover:underline ml-1">ลงทะเบียนที่นี่</router-link>
        </div>

      </div>
    </div>

    <footer class="text-center py-6 text-xs text-gray-400">
      &copy; 2025 UEvent Project. All Rights Reserved.
    </footer>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../services/api.js'

const router = useRouter()
const route = useRoute()
const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)
const showMobileMenu = ref(false)

watch(() => route.path, () => {
  showMobileMenu.value = false
})

const handleLogin = async () => {
  error.value = ""

  if (!username.value || !password.value) {
    error.value = "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน"
    return
  }

  try {
    isLoading.value = true
    
    // 1. Login เพื่อรับ Token
    const res = await apiClient.post('/auth/login/', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    localStorage.removeItem('isAdmin') // ล้างค่าเก่าที่อาจค้างอยู่

    // 2. ดึง Profile เพื่อเช็คสถานะ Organizer ทันที
    try {
      const profileRes = await apiClient.get('/auth/me/')
      const status = profileRes.data.organizer_status || 'none'
      localStorage.setItem('organizer_status', status)
    } catch (e) {
      console.warn('Failed to fetch profile status')
      localStorage.setItem('organizer_status', 'none')
    }

    // 3. ไปหน้า Home
    window.dispatchEvent(new Event('storage'))
    
    setTimeout(() => {
      router.push('/')
    }, 100)

  } catch (err) {
    console.error(err)
    error.value = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
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

.animate-fade-up { animation: fadeUp 0.6s ease-out; }
.animate-pulse-slow { animation: pulseSlow 6s infinite; }
.animate-shake { animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulseSlow { 
  0%, 100% { opacity: 0.4; transform: scale(1); } 
  50% { opacity: 0.6; transform: scale(1.05); } 
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}

@keyframes fade-in-down {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in-down {
  animation: fade-in-down 0.2s ease-out;
}
</style>