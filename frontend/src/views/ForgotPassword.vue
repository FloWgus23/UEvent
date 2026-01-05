<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F] flex flex-col">
    
    <nav class="fixed top-0 w-full z-50 bg-gradient-to-r from-[#0F172A] via-[#1E3A8A] to-[#1E40AF] text-white shadow-lg border-b border-white/10 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="text-2xl font-bold tracking-tight flex items-center gap-2 hover:opacity-90 transition-opacity">
            <i class="fa-solid fa-calendar-star text-white text-2xl drop-shadow-md"></i>
            <span class="font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-100">UEvent</span>
          </router-link>
        </div>
      </div>
    </nav>

    <div class="flex-grow flex items-center justify-center px-6 pt-24 pb-12 relative overflow-hidden">
      <div class="absolute top-0 left-1/4 w-[600px] h-[600px] bg-blue-200/40 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>
      <div class="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-indigo-200/40 rounded-full blur-[100px] pointer-events-none"></div>

      <div class="bg-white/90 backdrop-blur-sm rounded-[2.5rem] shadow-2xl w-full max-w-md p-8 md:p-12 relative z-10 animate-fade-up border border-white/50">
        
        <Transition name="fade" mode="out-in">
          
          <div v-if="!token" key="request-form">
            <div class="text-center mb-10">
              <i class="fa-solid fa-key text-6xl mb-6 bg-clip-text text-transparent bg-gradient-to-br from-blue-500 to-indigo-600 drop-shadow-sm"></i>
              <h2 class="text-3xl font-extrabold text-gray-900 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-700">
                ลืมรหัสผ่าน?
              </h2>
              <p class="text-gray-500 text-base mt-3 leading-relaxed">
                ไม่ต้องกังวล ระบุอีเมลของคุณเพื่อรับลิงก์สำหรับตั้งรหัสผ่านใหม่
              </p>
            </div>

            <form @submit.prevent="handleResetRequest" class="space-y-6">
              <div class="space-y-2">
                <label for="email" class="text-sm font-bold text-gray-700 ml-1">อีเมล</label>
                <div class="relative group">
                  <i class="fa-regular fa-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-blue-500 transition-colors"></i>
                  <input
                    id="email"
                    v-model="email"
                    type="email"
                    class="w-full pl-12 pr-4 py-3.5 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all text-gray-800 font-medium"
                    placeholder="ex. user@example.com"
                    required
                  />
                </div>
              </div>

              <div v-if="message" :class="`p-4 rounded-2xl flex items-start gap-3 text-sm font-medium ${status === 'success' ? 'bg-blue-50/80 text-blue-700 border border-blue-100' : 'bg-red-50/80 text-red-600 border border-red-100 animate-shake'}`">
                <i :class="`fa-solid text-lg mt-0.5 ${status === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation'}`"></i>
                <span class="leading-snug">{{ message }}</span>
              </div>

              <button
                type="submit"
                :disabled="isLoading"
                class="w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-lg rounded-2xl shadow-lg shadow-blue-500/30 transition-all transform hover:-translate-y-1 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-3"
              >
                <i v-if="isLoading" class="fa-solid fa-circle-notch fa-spin"></i>
                <span>{{ isLoading ? 'กำลังส่งข้อมูล...' : 'ส่งลิงก์รีเซ็ต' }}</span>
              </button>
            </form>
            
            <div class="text-center mt-8 text-sm text-gray-500">
              นึกรหัสผ่านออกแล้ว? 
              <router-link to="/login" class="text-blue-600 font-bold hover:text-blue-800 transition-colors underline-offset-2 hover:underline ml-1">
                เข้าสู่ระบบ
              </router-link>
            </div>
          </div>

          <div v-else key="confirm-form">
            <div class="text-center mb-10">
              <i class="fa-solid fa-lock-open text-6xl mb-6 bg-clip-text text-transparent bg-gradient-to-br from-green-500 to-teal-600 drop-shadow-sm"></i>
              <h2 class="text-3xl font-extrabold text-gray-900 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-700">
                ตั้งรหัสผ่านใหม่
              </h2>
              <p class="text-gray-500 text-base mt-3 leading-relaxed">
                สร้างรหัสผ่านใหม่ที่ปลอดภัยสำหรับการเข้าใช้งาน
              </p>
            </div>

            <form @submit.prevent="handlePasswordConfirm" class="space-y-6">
              <div class="space-y-2">
                <label class="text-sm font-bold text-gray-700 ml-1">รหัสผ่านใหม่</label>
                <div class="relative group">
                  <i class="fa-solid fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-green-500 transition-colors"></i>
                  <input
                    v-model="newPassword"
                    type="password"
                    class="w-full pl-12 pr-4 py-3.5 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:outline-none focus:border-green-500 focus:ring-4 focus:ring-green-500/10 transition-all text-gray-800 font-medium"
                    placeholder="ความยาวอย่างน้อย 6 ตัวอักษร"
                    required
                  />
                </div>
              </div>

              <div class="space-y-2">
                <label class="text-sm font-bold text-gray-700 ml-1">ยืนยันรหัสผ่าน</label>
                <div class="relative group">
                  <i class="fa-solid fa-check-double absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-green-500 transition-colors"></i>
                  <input
                    v-model="confirmPassword"
                    type="password"
                    class="w-full pl-12 pr-4 py-3.5 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:outline-none focus:border-green-500 focus:ring-4 focus:ring-green-500/10 transition-all text-gray-800 font-medium"
                    placeholder="กรอกรหัสผ่านเดิมอีกครั้ง"
                    required
                  />
                </div>
              </div>

              <div v-if="message" :class="`p-4 rounded-2xl flex items-start gap-3 text-sm font-medium ${status === 'success' ? 'bg-green-50/80 text-green-700 border border-green-100' : 'bg-red-50/80 text-red-600 border border-red-100 animate-shake'}`">
                <i :class="`fa-solid text-lg mt-0.5 ${status === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation'}`"></i>
                <span class="leading-snug">{{ message }}</span>
              </div>

              <button
                type="submit"
                :disabled="isLoading"
                class="w-full py-4 bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 text-white font-bold text-lg rounded-2xl shadow-lg shadow-green-500/30 transition-all transform hover:-translate-y-1 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-3"
              >
                <i v-if="isLoading" class="fa-solid fa-circle-notch fa-spin"></i>
                <span>{{ isLoading ? 'กำลังบันทึก...' : 'เปลี่ยนรหัสผ่าน' }}</span>
              </button>
            </form>
          </div>
        </Transition>

      </div>
    </div>
    <footer class="text-center py-6 text-xs text-gray-400">&copy; 2025 UEvent Project. All Rights Reserved.</footer>
  </div>
</template>

<script setup>
// ... (ส่วน Script เหมือนเดิมทุกประการครับ ไม่ต้องแก้)
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '../services/api.js'

const route = useRoute()
const router = useRouter()

// ตรวจสอบว่ามี Token ส่งมาใน URL หรือไม่
const token = ref(route.query.token || null)

// ตัวแปรสำหรับฟอร์ม
const email = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const message = ref('')
const status = ref('') // 'success' | 'error'
const isLoading = ref(false)

// 1. ฟังก์ชันขอลิงก์ (Request)
const handleResetRequest = async () => {
  message.value = ""
  status.value = ""
  if (!email.value) return

  try {
    isLoading.value = true
    await apiClient.post('/auth/password_reset/', { email: email.value })
    status.value = "success"
    message.value = "ระบบได้ส่งลิงก์รีเซ็ตรหัสผ่านไปที่อีเมลของคุณแล้ว"
    email.value = "" 
  } catch (err) {
    status.value = "error"
    message.value = 'ไม่พบอีเมลนี้ในระบบ หรือเกิดข้อผิดพลาด'
  } finally {
    isLoading.value = false
  }
}

// 2. ฟังก์ชันเปลี่ยนรหัสผ่าน (Confirm)
const handlePasswordConfirm = async () => {
  message.value = ""
  status.value = ""

  if (newPassword.value !== confirmPassword.value) {
    status.value = "error"
    message.value = "รหัสผ่านไม่ตรงกัน"
    return
  }
   
  if (newPassword.value.length < 6) {
    status.value = "error"
    message.value = "รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร"
    return
  }

  try {
    isLoading.value = true
    
    // ยิงไปที่ Endpoint confirm ของ django-rest-passwordreset
    await apiClient.post('/auth/password_reset/confirm/', {
      password: newPassword.value,
      token: token.value
    })

    status.value = "success"
    message.value = "เปลี่ยนรหัสผ่านสำเร็จ! กำลังพาไปหน้าเข้าสู่ระบบ..."
    
    // พาไปหน้า Login อัตโนมัติใน 2 วินาที
    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (err) {
    console.error(err)
    status.value = "error"
    message.value = "ลิงก์หมดอายุหรือเกิดข้อผิดพลาด กรุณาขอลิงก์ใหม่"
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

/* Animation พื้นฐาน */
.animate-fade-up { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1); }
.animate-pulse-slow { animation: pulseSlow 8s infinite; }
.animate-shake { animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both; }

/* Transition สำหรับการสลับหน้า (สำคัญมาก) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@keyframes fadeUp { 
  from { opacity: 0; transform: translateY(30px); } 
  to { opacity: 1; transform: translateY(0); } 
}
@keyframes pulseSlow { 
  0%, 100% { opacity: 0.3; transform: scale(1); } 
  50% { opacity: 0.5; transform: scale(1.05); } 
}
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
</style>