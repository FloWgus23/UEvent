<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F]">
    
    <nav class="fixed top-0 w-full z-40 bg-gradient-to-r from-[#0F172A] via-[#1E3A8A] to-[#1E40AF] text-white shadow-lg border-b border-white/10 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <button 
            @click="router.back()" 
            class="w-9 h-9 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 text-white transition-all backdrop-blur-sm border border-white/20"
          >
            <i class="fa-solid fa-arrow-left text-sm"></i>
          </button>
          <h1 class="text-xl font-bold tracking-wide">การแจ้งเตือน</h1>
        </div>
        
        <div class="hidden md:flex items-center gap-2 opacity-80">
          <i class="fa-solid fa-calendar-star text-lg"></i>
          <span class="font-bold">UEvent</span>
        </div>
      </div>
    </nav>

    <div class="pt-28 pb-12 px-4">
      <div class="max-w-3xl mx-auto">
        
        <div class="flex justify-between items-end mb-8 px-2">
          <div>
            <h2 class="text-3xl font-bold text-gray-900 tracking-tight flex items-center gap-2">
              <span class="w-2 h-8 bg-blue-600 rounded-full inline-block"></span>
              รายการล่าสุด
            </h2>
            <p class="text-gray-500 text-sm mt-1 ml-4">อัปเดตกิจกรรมและสถานะของคุณ</p>
          </div>
          
          <button 
            v-if="unreadCount > 0"
            @click="markAllAsRead"
            class="flex items-center gap-2 text-sm font-semibold text-blue-600 hover:text-white bg-blue-50 hover:bg-blue-600 px-5 py-2.5 rounded-full transition-all shadow-sm hover:shadow-md active:scale-95 group"
          >
            <i class="fa-solid fa-check-double text-xs group-hover:text-white transition-colors"></i>
            อ่านทั้งหมด
          </button>
        </div>

        <div v-if="isLoading" class="flex flex-col items-center justify-center py-24">
          <div class="w-12 h-12 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin"></div>
          <p class="mt-4 text-gray-400 font-medium animate-pulse">กำลังโหลดข้อมูล...</p>
        </div>

        <div v-else-if="notifications.length === 0" class="text-center py-24 bg-white rounded-[32px] border border-dashed border-gray-200 shadow-sm mx-2">
          <div class="w-24 h-24 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <i class="fa-regular fa-bell-slash text-4xl text-blue-300"></i>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">ไม่มีการแจ้งเตือน</h3>
          <p class="text-gray-500 text-sm max-w-xs mx-auto">คุณจะได้รับการแจ้งเตือนเมื่อมีกิจกรรมใหม่ๆ หรือมีการอัปเดตสถานะ</p>
        </div>

        <div v-else class="space-y-4">
          <transition-group name="list">
            <div 
              v-for="notify in notifications" 
              :key="notify.id"
              @click="readNotification(notify)"
              class="group relative bg-white hover:bg-gray-50 border border-gray-100 rounded-2xl p-5 transition-all duration-300 cursor-pointer flex gap-5 items-start shadow-[0_2px_8px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] hover:-translate-y-0.5 overflow-hidden"
              :class="{ 'bg-blue-50/60 border-blue-200/60': !notify.is_read }"
            >
              <div v-if="!notify.is_read" class="absolute left-0 top-0 bottom-0 w-1.5 bg-blue-600"></div>

              <div 
                class="flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center text-lg shadow-sm mt-1 transition-transform group-hover:scale-105"
                :class="getIconStyle(notify.notification_type)"
              >
                <i :class="getIconClass(notify.notification_type)"></i>
              </div>

              <div class="flex-grow min-w-0 pt-0.5">
                <div class="flex justify-between items-start mb-1.5">
                  <h4 
                    class="text-[16px] leading-snug pr-4 transition-colors group-hover:text-blue-700" 
                    :class="!notify.is_read ? 'font-bold text-gray-900' : 'font-medium text-gray-700'"
                  >
                    {{ notify.title }}
                  </h4>
                  <span class="text-xs text-gray-400 whitespace-nowrap flex-shrink-0 ml-2 font-medium bg-gray-100 px-2 py-1 rounded-full border border-gray-100">
                    {{ formatTime(notify.created_at) }}
                  </span>
                </div>
                <p class="text-sm text-gray-500 leading-relaxed line-clamp-2">
                  {{ notify.message }}
                </p>
              </div>

              <div v-if="!notify.is_read" class="absolute top-6 right-6">
                <span class="relative flex h-2.5 w-2.5">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-600"></span>
                </span>
              </div>
            </div>
          </transition-group>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import notificationService from '@/services/notificationService.js'

const router = useRouter()
const isLoading = ref(false)
const notifications = ref([])

// นับจำนวนที่ยังไม่อ่าน
const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

// ⭐ Helpers ปรับปรุงใหม่ (ใช้ Gradient และ Border)
const getIconStyle = (type) => {
  switch(type) {
    case 'success': return 'bg-gradient-to-br from-green-50 to-green-100 text-green-600 border border-green-200'
    case 'error': return 'bg-gradient-to-br from-red-50 to-red-100 text-red-600 border border-red-200'
    case 'warning': return 'bg-gradient-to-br from-orange-50 to-orange-100 text-orange-600 border border-orange-200'
    default: return 'bg-gradient-to-br from-blue-50 to-blue-100 text-blue-600 border border-blue-200' 
  }
}

// ⭐ เปลี่ยน Icon ให้สื่อความหมายมากขึ้น
const getIconClass = (type) => {
  switch(type) {
    case 'success': return 'fa-solid fa-check'
    case 'error': return 'fa-solid fa-circle-exclamation'
    case 'warning': return 'fa-solid fa-clock' // ใช้รูปนาฬิกาสำหรับการเตือน
    default: return 'fa-solid fa-bell' 
  }
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (minutes < 1) return 'เมื่อสักครู่'
  if (minutes < 60) return `${minutes} นาทีที่แล้ว`
  if (hours < 24) return `${hours} ชม. ที่แล้ว`
  if (days < 7) return `${days} วันที่แล้ว`
  
  return date.toLocaleDateString('th-TH', {
    day: 'numeric', month: 'short', year: '2-digit'
  })
}

// API Actions
const fetchNotifications = async () => {
  try {
    isLoading.value = true
    const response = await notificationService.getMyNotifications()
    const data = Array.isArray(response.data) ? response.data : (response.data.results || [])
    notifications.value = data
  } catch (error) {
    console.error("Failed to fetch notifications:", error)
  } finally {
    isLoading.value = false
  }
}

const markAllAsRead = async () => {
  try {
    notifications.value.forEach(n => n.is_read = true)
    await notificationService.markAllRead()
  } catch (error) {
    console.error("Error marking all read:", error)
  }
}

const readNotification = async (notify) => {
  if (!notify.is_read) {
    try {
      notify.is_read = true 
      await notificationService.markAsRead(notify.id)
    } catch (error) {
      console.error("Error marking read:", error)
      notify.is_read = false 
    }
  }
}

onMounted(() => {
  fetchNotifications()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>