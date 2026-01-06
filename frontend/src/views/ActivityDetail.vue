<template>
  <div class="min-h-screen bg-gray-50 pb-12">
    <nav class="bg-[#1E3A8A] text-white p-4 shadow-md">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <router-link to="/" class="text-2xl font-bold tracking-tight flex items-center gap-2 hover:opacity-90 transition-opacity">
            <i class="fa-solid fa-calendar-star text-white text-xl drop-shadow-md"></i>
            <span class="font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-100">UEvent</span>
        </router-link>
        <router-link to="/" class="text-blue-200 hover:text-white transition-colors flex items-center gap-1">
          <i class="fa-solid fa-chevron-left text-sm"></i> กลับหน้าแรก
        </router-link>
      </div>
    </nav>

    <div v-if="isLoading" class="flex flex-col items-center justify-center py-24 text-gray-500 space-y-4 animate-pulse">
      <i class="fa-solid fa-circle-notch fa-spin text-4xl text-blue-300"></i>
      <p>กำลังโหลดข้อมูลกิจกรรม...</p>
    </div>

    <div v-else-if="activity" class="max-w-5xl mx-auto mt-8 bg-white rounded-3xl shadow-2xl overflow-hidden animate-fade-up">
      
      <div class="h-96 w-full relative group overflow-hidden">
        <img 
          :src="activity.image || 'https://via.placeholder.com/1200x600?text=Activity+Banner'" 
          class="w-full h-full object-cover transform transition-transform duration-700 group-hover:scale-105"
          alt="Activity Banner"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent p-8 flex flex-col justify-end">
          
          <div class="flex flex-wrap gap-3 mb-4 animate-slide-up delay-100">
            
            <span v-if="activityStatus === 'ended'" class="px-4 py-1.5 bg-red-600/90 text-white backdrop-blur-sm rounded-full text-sm font-bold shadow-sm flex items-center gap-2">
               <i class="fa-solid fa-flag-checkered"></i> สิ้นสุดแล้ว
            </span>

            <span v-else-if="activityStatus === 'ongoing'" class="px-4 py-1.5 bg-blue-600/90 text-white backdrop-blur-sm rounded-full text-sm font-bold shadow-sm flex items-center gap-2">
               <i class="fa-solid fa-play-circle animate-pulse"></i> กำลังดำเนินการ
            </span>

            <span v-else-if="activity.registered_count >= activity.capacity" class="px-4 py-1.5 bg-orange-500/90 text-white backdrop-blur-sm rounded-full text-sm font-bold shadow-sm flex items-center gap-2">
               <i class="fa-solid fa-users-slash"></i> ที่นั่งเต็ม
            </span>

            <span v-else class="px-4 py-1.5 bg-green-500/90 text-white backdrop-blur-sm rounded-full text-sm font-bold shadow-sm flex items-center gap-2">
               <i class="fa-solid fa-ticket"></i> เปิดรับสมัคร
            </span>
            
            <span v-if="activity.category" class="px-4 py-1.5 bg-blue-600/80 text-white backdrop-blur-sm rounded-full text-sm font-semibold shadow-sm flex items-center gap-2">
               <i :class="getCategoryIcon(activity.category)"></i> {{ activity.category }}
            </span>
          </div>

          <h1 class="text-4xl md:text-5xl font-extrabold text-white drop-shadow-2xl leading-tight animate-slide-up delay-200">{{ activity.name }}</h1>
        </div>
      </div>

      <div class="p-8 md:p-10 grid grid-cols-1 lg:grid-cols-3 gap-10">
        
        <div class="lg:col-span-2 space-y-8">
          <div class="flex items-center gap-4 pb-6 border-b border-gray-100">
            <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 text-xl shadow-sm">
              <i class="fa-solid fa-user-tie"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium mb-0.5">ผู้จัดกิจกรรม</p>
              <h3 class="text-lg font-bold text-gray-900">{{ activity.organizer || 'ไม่ระบุ' }}</h3>
            </div>
          </div>
          
          <div>
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <i class="fa-solid fa-circle-info text-blue-500"></i>
              รายละเอียดกิจกรรม
            </h2>
            <div class="prose max-w-none text-gray-600 leading-relaxed whitespace-pre-line pl-4 border-l-4 border-blue-100 py-2">
              {{ activity.description || 'ไม่มีรายละเอียดเพิ่มเติม' }}
            </div>
          </div>

          <div v-if="activity.tags" class="pt-4">
             <h3 class="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
               <i class="fa-solid fa-tags text-blue-500"></i>
               แท็กที่เกี่ยวข้อง
             </h3>
            <div class="flex gap-2 flex-wrap">
              <span 
                v-for="tag in activity.tags.split(',')" 
                :key="tag"
                class="px-4 py-1.5 bg-gray-100 hover:bg-blue-50 text-gray-600 hover:text-blue-700 rounded-full text-sm font-medium transition-colors cursor-default border border-transparent hover:border-blue-200"
              >
                #{{ tag.trim() }}
              </span>
            </div>
          </div>
        </div>

        <div class="lg:col-span-1">
          <div class="bg-gradient-to-br from-white to-blue-50 rounded-[2rem] p-7 border border-blue-100 shadow-lg sticky top-8 space-y-7">
            
            <div class="space-y-5">
              <div class="flex items-start gap-4">
                <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                   <i class="fa-regular fa-calendar-days text-lg"></i>
                </div>
                <div>
                  <p class="text-sm font-medium text-blue-900">วันที่จัดกิจกรรม</p>
                  <p class="font-semibold text-gray-700 text-lg">{{ formatDate(activity.date) }}</p>
                </div>
              </div>
              <div class="flex items-start gap-4">
                <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                  <i class="fa-regular fa-clock text-lg"></i>
                </div>
                <div>
                   <p class="text-sm font-medium text-blue-900">เวลา</p>
                   <p class="font-semibold text-gray-700 text-lg">{{ activity.time_display || 'ไม่ระบุเวลา' }}</p>
                </div>
              </div>
              <div class="flex items-start gap-4">
                <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                  <i class="fa-solid fa-location-dot text-lg"></i>
                </div>
                 <div>
                   <p class="text-sm font-medium text-blue-900">สถานที่</p>
                   <p class="font-semibold text-gray-700 leading-tight">{{ activity.location || 'ไม่ระบุสถานที่' }}</p>
                </div>
              </div>
              
              <div class="pt-4 border-t border-blue-100/50">
                 <div class="flex justify-between items-end mb-2">
                    <span class="text-sm font-medium text-blue-900 flex items-center gap-1">
                      <i class="fa-solid fa-user-group text-blue-500"></i> จำนวนผู้เข้าร่วม
                    </span>
                    <span class="font-bold text-gray-700">
                      <span :class="{'text-red-500': activity.registered_count >= activity.capacity, 'text-blue-600': activity.registered_count < activity.capacity}">{{ activity.registered_count }}</span>
                      <span class="text-gray-400 text-sm">/{{ activity.capacity }}</span>
                    </span>
                 </div>
                 <div class="h-3 bg-blue-100 rounded-full overflow-hidden shadow-inner">
                   <div 
                      :class="['h-full rounded-full transition-all duration-1000 ease-out relative overflow-hidden', 
                               activityStatus === 'ended' ? 'bg-gradient-to-r from-red-500 to-orange-500' :
                               activity.registered_count >= activity.capacity ? 'bg-gradient-to-r from-orange-500 to-red-500' : 
                               'bg-gradient-to-r from-blue-500 to-teal-400']"
                      :style="`width: ${Math.min((activity.registered_count / activity.capacity) * 100, 100)}%`"
                   >
                     <div v-if="activityStatus === 'upcoming' && activity.registered_count < activity.capacity" class="absolute inset-0 bg-white/30 animate-shimmer" style="transform: skewX(-20deg);"></div>
                   </div>
                 </div>
               </div>
            </div>

            <div class="pt-2">
              <template v-if="isLoggedIn">
                
                <!-- ⭐ เพิ่ม: แสดงถ้าเป็นผู้จัดกิจกรรม -->
                <div v-if="isActivityOwner" class="space-y-4 animate-fade-in">
                  <div class="bg-blue-50 border-2 border-blue-200 rounded-2xl p-5 text-center relative overflow-hidden shadow-sm">
                    <div class="absolute -right-4 -top-4 text-blue-100 text-6xl z-0 opacity-50">
                      <i class="fa-solid fa-user-tie"></i>
                    </div>
                    <div class="relative z-10">
                      <div class="flex items-center justify-center gap-2 text-blue-700 font-extrabold text-xl mb-2">
                        <i class="fa-solid fa-crown text-2xl text-yellow-500"></i>
                        <span>คุณเป็นผู้จัดกิจกรรมนี้</span>
                      </div>
                      <p class="text-blue-600 text-sm font-medium">
                        คุณไม่สามารถลงทะเบียนกิจกรรมของตัวเองได้
                      </p>
                    </div>
                  </div>

                  <router-link
                    to="/organizer/dashboard"
                    class="block w-full py-3.5 text-center rounded-2xl font-bold text-lg shadow-md transition-all transform hover:-translate-y-1 active:scale-95 text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 group"
                  >
                    <span>จัดการกิจกรรม</span>
                    <i class="fa-solid fa-arrow-right ml-2 group-hover:translate-x-1 transition-transform"></i>
                  </router-link>
                </div>

                <!-- แสดงถ้าลงทะเบียนแล้ว -->
                <div v-else-if="isRegistered" class="space-y-4 animate-fade-in">
                  <div class="bg-green-50 border border-green-200 rounded-2xl p-4 text-center relative overflow-hidden shadow-sm">
                    <div class="absolute -right-4 -top-4 text-green-100 text-6xl z-0 opacity-50">
                      <i class="fa-solid fa-circle-check"></i>
                    </div>
                    <div class="relative z-10">
                      <div class="flex items-center justify-center gap-2 text-green-700 font-extrabold text-xl mb-1">
                        <i class="fa-solid fa-circle-check text-2xl animate-bounce-small"></i>
                        <span>คุณลงทะเบียนแล้ว!</span>
                      </div>
                      <p class="text-green-600 text-sm font-medium opacity-90">
                        เมื่อ: {{ formatDateTime(registrationDate) }}
                      </p>
                    </div>
                  </div>

                  <router-link
                    to="/profile/activities"
                    class="block w-full py-3.5 text-center rounded-2xl font-bold text-lg shadow-md transition-all transform hover:-translate-y-1 active:scale-95 text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 group"
                  >
                    <span>ดูกิจกรรมของฉัน</span>
                    <i class="fa-solid fa-arrow-right ml-2 group-hover:translate-x-1 transition-transform"></i>
                  </router-link>
                </div>

                <div v-else>
                  
                  <button 
                    v-if="activityStatus === 'ended'"
                    disabled
                    class="w-full py-4 rounded-2xl font-bold text-xl text-white shadow-lg bg-gradient-to-r from-red-500 to-orange-500 cursor-not-allowed relative overflow-hidden group"
                  >
                    <div class="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors"></div>
                    <div class="flex items-center justify-center gap-3 relative z-10">
                       <i class="fa-solid fa-flag-checkered text-2xl animate-wave drop-shadow-sm"></i>
                       <span class="tracking-wider drop-shadow-sm">สิ้นสุดแล้ว</span>
                    </div>
                  </button>

                  <button 
                    v-else-if="activityStatus === 'ongoing'"
                    disabled
                    class="w-full py-4 rounded-2xl font-bold text-xl text-white shadow-lg bg-gradient-to-r from-blue-500 to-indigo-500 cursor-not-allowed relative overflow-hidden"
                  >
                    <div class="flex items-center justify-center gap-3">
                       <i class="fa-solid fa-spinner fa-spin text-2xl"></i>
                       <span class="tracking-wide">กำลังดำเนินการ</span>
                    </div>
                    <div class="absolute inset-0 bg-white/10 animate-pulse"></div>
                  </button>

                  <button 
                    v-else-if="activity.registered_count >= activity.capacity"
                    disabled
                    class="w-full py-3.5 rounded-2xl font-bold text-lg shadow-md text-white bg-red-400 cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    <i class="fa-solid fa-users-slash text-xl"></i>
                    <span>ที่นั่งเต็มแล้ว</span>
                  </button>

                  <button 
                    v-else
                    @click="handleRegisterClick"
                    class="w-full py-4 rounded-2xl font-bold text-xl shadow-lg transition-all transform hover:-translate-y-1 active:scale-95 text-white bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 flex items-center justify-center gap-2 relative overflow-hidden group"
                  >
                     <span class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></span>
                     <i class="fa-solid fa-ticket text-2xl relative z-10 group-hover:rotate-12 transition-transform"></i>
                     <span class="relative z-10 tracking-wide">ลงทะเบียนเข้าร่วม</span>
                  </button>
                </div>

              </template>

              <button 
                v-else
                @click="$router.push('/login')"
                class="w-full py-3.5 rounded-2xl font-bold text-lg shadow-md text-white bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 transition-all transform hover:-translate-y-1 flex items-center justify-center gap-2"
              >
                <i class="fa-solid fa-right-to-bracket"></i>
                เข้าสู่ระบบเพื่อลงทะเบียน
              </button>
            </div>

          </div>
        </div>

      </div>
    </div>

    <div v-else class="flex flex-col items-center justify-center py-24 text-red-400 space-y-4 animate-fade-up">
      <i class="fa-regular fa-circle-xmark text-6xl opacity-50"></i>
      <p class="text-xl font-medium">ไม่พบข้อมูลกิจกรรมที่คุณต้องการ</p>
      <router-link to="/" class="px-6 py-2 bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors font-medium">
        กลับหน้าแรก
      </router-link>
    </div>

    <Transition name="modal">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showModal = false"></div>

        <div class="relative bg-white rounded-[2rem] shadow-2xl w-full max-w-lg overflow-hidden animate-scale-up">
          
          <div class="bg-gradient-to-r from-blue-800 to-blue-600 px-8 py-5 flex justify-between items-center relative overflow-hidden">
             <div class="absolute -left-10 -top-10 text-white/10 text-8xl">
               <i class="fa-solid fa-ticket"></i>
             </div>
            <h3 class="text-2xl font-bold text-white flex items-center gap-3 relative z-10">
               <i class="fa-solid fa-clipboard-check"></i>
               ยืนยันการลงทะเบียน
            </h3>
            <button @click="showModal = false" class="text-blue-100 hover:text-white text-3xl font-bold transition-colors relative z-10 leading-none">&times;</button>
          </div>

          <div class="p-8 space-y-6">
            <p class="text-gray-600 font-medium">
              กรุณาตรวจสอบข้อมูลและกรอกรายละเอียดเพิ่มเติม (ถ้ามี)
            </p>

            <div class="bg-blue-50/50 p-5 rounded-2xl space-y-3 border border-blue-100">
              <div class="flex items-center gap-3">
                 <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                    <i class="fa-regular fa-user"></i>
                 </div>
                <div class="flex-grow">
                   <p class="text-xs text-blue-500 font-medium">ชื่อผู้สมัคร</p>
                   <p class="font-bold text-gray-800 text-lg">{{ userProfile.fullname || 'ไม่ระบุ' }}</p>
                </div>
              </div>
               <div class="flex items-center gap-3">
                 <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                    <i class="fa-regular fa-envelope"></i>
                 </div>
                 <div class="flex-grow">
                   <p class="text-xs text-blue-500 font-medium">อีเมล</p>
                   <p class="font-semibold text-gray-700 truncate">{{ userProfile.email || 'ไม่ระบุ' }}</p>
                </div>
              </div>
            </div>

            <div class="space-y-5">
              <div class="space-y-1">
                <label class="block text-sm font-bold text-gray-700 ml-1">
                  เบอร์โทรศัพท์ติดต่อ <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                  <i class="fa-solid fa-phone absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                  <input 
                    v-model="form.phone" 
                    type="tel" 
                    class="w-full pl-11 pr-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all font-medium text-gray-700"
                    placeholder="เช่น 081-234-5678"
                  >
                </div>
              </div>
              
              <div class="space-y-1">
                <label class="block text-sm font-bold text-gray-700 ml-1">
                  หมายเหตุถึงผู้จัด (ถ้ามี)
                </label>
                <div class="relative">
                   <i class="fa-regular fa-comment-dots absolute left-4 top-4 text-gray-400"></i>
                  <textarea 
                    v-model="form.note" 
                    rows="3"
                    class="w-full pl-11 pr-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all resize-none font-medium text-gray-700"
                    placeholder="เช่น แพ้อาหารทะเล, นำรถส่วนตัวมา"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <div class="px-8 py-5 bg-gray-50 flex gap-4 justify-end border-t border-gray-100">
            <button 
              @click="showModal = false"
              class="px-6 py-2.5 text-gray-600 hover:bg-gray-100 rounded-xl transition-colors font-bold"
            >
              ยกเลิก
            </button>
            <button 
              @click="confirmRegistration"
              :disabled="isSubmitting"
              class="px-6 py-2.5 bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 text-white rounded-xl font-bold shadow-md transition-all transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-3"
            >
              <i v-if="!isSubmitting" class="fa-solid fa-check"></i>
              <span v-if="isSubmitting" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
              <span>{{ isSubmitting ? 'กำลังบันทึก...' : 'ยืนยันการลงทะเบียน' }}</span>
            </button>
          </div>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import activityService from '@/services/activityService'
import apiClient from '@/services/api.js'

// --- Helper Functions ---
const getCategoryIcon = (categoryName) => {
    const iconMap = {
        'วิชาการ': 'fa-solid fa-book-open',
        'สันทนาการ': 'fa-solid fa-guitar',
        'กีฬา': 'fa-solid fa-basketball',
        'ศิลปะและวัฒนธรรม': 'fa-solid fa-palette',
        'บำเพ็ญประโยชน์': 'fa-solid fa-hand-holding-heart',
        'เทคโนโลยี': 'fa-solid fa-microchip',
        'ทั่วไป': 'fa-solid fa-star',
    };
    return iconMap[categoryName] || 'fa-solid fa-tag';
};

const route = useRoute()
const router = useRouter()

const activity = ref(null)
const isLoading = ref(true)
const isLoggedIn = ref(false)
const currentUserId = ref(null)  // ⭐ เพิ่ม: เก็บ user id ของผู้ใช้ปัจจุบัน

const isRegistered = ref(false)
const registrationDate = ref(null)

const showModal = ref(false)
const isSubmitting = ref(false)
const userProfile = ref({}) 
const form = ref({
  phone: '',
  note: ''
})

// ⭐ เพิ่ม: Computed เช็คว่าเป็นเจ้าของกิจกรรมหรือไม่
const isActivityOwner = computed(() => {
  if (!activity.value || !currentUserId.value) return false
  return activity.value.owner_id === currentUserId.value
})

// Computed: Activity Status Logic (เช็คเวลาจริง)
const activityStatus = computed(() => {
  if (!activity.value) return 'loading'
  if (activity.value.status === 'สิ้นสุดแล้ว') return 'ended'
  if (!activity.value.date) return 'upcoming' // ไม่ระบุวัน ถือว่าเปิดตลอด

  const now = new Date()
  const date = new Date(activity.value.date)
  
  // สร้าง DateTime เริ่มต้น
  const startDateTime = new Date(date)
  if (activity.value.start_time) {
      const [sh, sm] = activity.value.start_time.split(':')
      startDateTime.setHours(parseInt(sh), parseInt(sm), 0)
  } else {
      startDateTime.setHours(0, 0, 0)
  }

  // สร้าง DateTime สิ้นสุด
  const endDateTime = new Date(date)
  if (activity.value.end_time) {
      const [eh, em] = activity.value.end_time.split(':')
      endDateTime.setHours(parseInt(eh), parseInt(em), 59)
  } else {
      endDateTime.setHours(23, 59, 59)
  }

  // เช็คสถานะตามเวลา
  if (now > endDateTime) {
      return 'ended'           // 🏁 จบแล้ว
  } else if (now >= startDateTime && now <= endDateTime) {
      return 'ongoing'         // ⚠️ กำลังดำเนินการ
  } else {
      return 'upcoming'        // ✅ ยังไม่ถึงเวลา (เปิดรับสมัคร)
  }
})

// Format Date Functions
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('th-TH', { 
    year: 'numeric', month: 'long', day: 'numeric' 
  })
}

const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const checkRegistrationStatus = async () => {
  if (!isLoggedIn.value) return
  
  try {
    const res = await activityService.checkRegistration(activity.value.id)
    isRegistered.value = res.data.is_registered
    if (res.data.is_registered) {
      registrationDate.value = res.data.registered_at
    }
  } catch (err) {
    console.error('ไม่สามารถเช็คสถานะได้:', err)
  }
}

const fetchDetail = async () => {
  try {
    const id = route.params.id
    const res = await activityService.getActivity(id)
    activity.value = res.data
    await checkRegistrationStatus()
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

const handleRegisterClick = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  try {
    const response = await apiClient.get('/user/profile/')
    const userData = response.data

    userProfile.value = {
        fullname: userData.fullname,
        email: userData.email
    }
    
    form.value.phone = userData.phone || '' 
    form.value.note = ''
    
    showModal.value = true 
  } catch (err) {
    console.error('Error fetching user profile:', err)
    alert('ไม่สามารถดึงข้อมูลผู้ใช้ได้ กรุณาลองใหม่')
  }
}

const confirmRegistration = async () => {
  if (!form.value.phone) {
    alert('กรุณากรอกเบอร์โทรศัพท์')
    return
  }

  try {
    isSubmitting.value = true
    
    await activityService.registerActivity(activity.value.id, {
        phone: form.value.phone,
        note: form.value.note
    })

    alert('✅ ลงทะเบียนสำเร็จเรียบร้อย!')
    showModal.value = false
    
    await fetchDetail()
    
  } catch (err) {
    console.error(err)
    // ⭐ แก้ไข: ดึง error message จาก backend (รองรับทั้ง error และ message)
    const errorMsg = err.response?.data?.error || err.response?.data?.message || 'เกิดข้อผิดพลาดในการลงทะเบียน'
    alert('❌ ' + errorMsg)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(async () => {
  isLoggedIn.value = !!localStorage.getItem('access')
  
  // ⭐ ถ้า login แล้ว ดึง user id
  if (isLoggedIn.value) {
    try {
      const response = await apiClient.get('/user/profile/')
      currentUserId.value = response.data.id
    } catch (err) {
      console.error('Error fetching user id:', err)
    }
  }
  
  fetchDetail()
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

/* Animations */
.animate-fade-up { animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; }
.animate-slide-up { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; opacity: 0; }
.animate-scale-up { animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.animate-bounce-small { animation: bounceSmall 2s infinite; }
.animate-wave { animation: wave 2.5s infinite ease-in-out; transform-origin: bottom center; }
.animate-shimmer {
  animation: shimmer 2s infinite linear;
  background: linear-gradient(to right, transparent 0%, rgba(255,255,255,0.4) 50%, transparent 100%);
  width: 50%;
}

@keyframes fadeUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
@keyframes bounceSmall { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
@keyframes wave { 0%, 100% { transform: rotate(0deg); } 25% { transform: rotate(-5deg); } 75% { transform: rotate(5deg); } }
@keyframes shimmer { from { transform: translateX(-150%) skewX(-20deg); } to { transform: translateX(350%) skewX(-20deg); } }

.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>