<template>
  <nav class="fixed top-0 w-full z-50 bg-gradient-to-r from-[#0F172A] via-[#1E3A8A] to-[#1E40AF] text-white shadow-lg border-b border-white/10 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        
        <router-link to="/" class="text-2xl font-bold tracking-tight flex items-center gap-2 hover:opacity-90 transition-opacity">
          <i class="fa-solid fa-calendar-star text-white text-2xl drop-shadow-md"></i>
          <span class="font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-100">UEvent</span>
        </router-link>

        <div class="flex items-center gap-8">
          <div class="hidden md:flex items-center gap-6 text-[15px] font-medium text-blue-100">
            <router-link to="/" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all" active-class="text-white bg-white/10 font-bold shadow-sm">หน้าแรก</router-link>
            <router-link to="/category" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all" active-class="text-white bg-white/10 font-bold shadow-sm">หมวดหมู่</router-link>
            <router-link to="/news" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all" active-class="text-white bg-white/10 font-bold shadow-sm">ข่าวสาร</router-link>
          </div>

          <button
            @click="showMobileMenu = !showMobileMenu"
            class="md:hidden text-white p-2 rounded-lg hover:bg-white/10 transition-colors"
            aria-label="เปิดเมนู"
          >
            <i :class="showMobileMenu ? 'fa-solid fa-xmark' : 'fa-solid fa-bars'" class="text-xl"></i>
          </button>

          <div v-if="isLoggedIn" class="flex items-center gap-4">
            
            <div class="relative">
              <button @click.stop="toggleNotificationDropdown" class="text-blue-200 hover:text-white transition-colors relative p-2 rounded-full hover:bg-white/10">
                <i class="fa-regular fa-bell text-xl"></i>
                <span v-if="unreadCount > 0" class="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-[#1E3A8A] animate-pulse"></span>
              </button>

              <div v-if="showNotificationDropdown" class="absolute right-0 mt-3 w-80 bg-white/95 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-gray-100 py-2 z-50 transform origin-top-right transition-all animate-scale-in overflow-hidden flex flex-col" @click.stop>
                
                <div class="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                  <h3 class="text-sm font-bold text-gray-800">การแจ้งเตือน</h3>
                  <button v-if="unreadCount > 0" @click="markAllAsRead" class="text-xs text-blue-600 hover:underline">อ่านทั้งหมด</button>
                </div>

                <div class="max-h-[350px] overflow-y-auto custom-scrollbar">
                  <div v-if="notifications.length === 0" class="p-8 text-center text-gray-400 text-sm">
                    <i class="fa-regular fa-bell-slash text-3xl mb-2 opacity-30 block"></i>
                    ไม่มีการแจ้งเตือนใหม่
                  </div>
                  <div 
                    v-for="item in notifications" 
                    :key="item.id"
                    :class="['px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-50 last:border-0 transition-colors flex gap-3 items-start relative group', !item.is_read ? 'bg-blue-50/40' : '']"
                    @click="markAsRead(item.id)"
                  >
                    <div class="mt-1 flex-shrink-0">
                       <i v-if="item.notification_type === 'success'" class="fa-solid fa-circle-check text-green-500 text-lg"></i>
                       <i v-else-if="item.notification_type === 'warning'" class="fa-solid fa-clock text-orange-500 text-lg"></i>
                       <i v-else class="fa-solid fa-circle-info text-blue-500 text-lg"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm text-gray-800 leading-tight mb-0.5" :class="{'font-bold': !item.is_read, 'font-medium': item.is_read}">{{ item.title }}</p>
                      <p class="text-xs text-gray-500 line-clamp-2 leading-snug">{{ item.message }}</p>
                      <p class="text-[10px] text-gray-400 mt-1.5">{{ formatNotificationDate(item.created_at) }}</p>
                    </div>
                    <div v-if="!item.is_read" class="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0 animate-pulse"></div>
                  </div>
                </div>

                <div class="p-2 border-t border-gray-100 bg-gray-50">
                  <router-link 
                    to="/notifications" 
                    class="block w-full py-2 text-center text-xs font-bold text-blue-600 hover:text-blue-700 hover:bg-blue-100/50 rounded-lg transition-colors"
                    @click="closeDropdown"
                  >
                    ดูการแจ้งเตือนทั้งหมด <i class="fa-solid fa-arrow-right ml-1"></i>
                  </router-link>
                </div>

              </div>
            </div>

            <div class="relative" ref="dropdownRef">
              <button @click="toggleDropdown" class="flex items-center gap-2 hover:opacity-90 transition-opacity">
                <div class="w-9 h-9 bg-white/10 rounded-full flex items-center justify-center border border-white/20 text-white overflow-hidden backdrop-blur-sm hover:bg-white/20 transition-all">
                  <img 
                    v-if="userProfile?.profile?.profile_image" 
                    :src="userProfile.profile.profile_image" 
                    alt="Profile"
                    class="w-full h-full object-cover"
                  />
                  <i v-else class="fa-solid fa-user text-sm"></i>
                </div>
              </button>

              <div v-if="showDropdown" class="absolute right-0 mt-3 w-64 bg-white/95 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-gray-100 py-2 z-50 transform origin-top-right transition-all animate-scale-in" @click.stop>
                <div class="px-5 py-3 border-b border-gray-100">
                  <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">บัญชีผู้ใช้</p>
                </div>
                <router-link to="/profile" class="dropdown-item" @click="closeDropdown">
                  <i class="fa-regular fa-id-card w-5 text-blue-600"></i> โปรไฟล์
                </router-link>
                <router-link to="/profile/activities" class="dropdown-item" @click="closeDropdown">
                  <i class="fa-regular fa-calendar-check w-5 text-green-600"></i> กิจกรรมของฉัน
                </router-link>
                <router-link to="/profile/dashboard" class="dropdown-item" @click="closeDropdown">
                  <i class="fa-solid fa-chart-line w-5 text-blue-600"></i> แดชบอร์ด
                </router-link>
                
                <div v-if="organizerStatus === 'approved'">
                  <router-link to="/organizer/dashboard" class="dropdown-item font-semibold text-purple-700 bg-purple-50/50" @click="closeDropdown">
                      <i class="fa-solid fa-gauge-high w-5"></i> ผู้จัดกิจกรรม
                  </router-link>
                </div>
                
                <div v-else-if="organizerStatus === 'pending'">
                   <router-link to="/waiting-approval" class="dropdown-item text-yellow-600 bg-yellow-50 hover:bg-yellow-100" @click="closeDropdown">
                      <i class="fa-solid fa-clock w-5"></i> รออนุมัติ
                   </router-link>
                </div>
                
                <div v-else>
                  <button @click="requestOrganizer" class="dropdown-item text-blue-600 hover:bg-blue-50 w-full text-left">
                      <i class="fa-solid fa-briefcase w-5"></i> สมัครเป็นผู้จัด
                  </button>
                </div>

                <div class="border-t border-gray-100 my-1"></div>
                <button @click="handleLogout" class="dropdown-item text-red-600 hover:bg-red-50">
                  <i class="fa-solid fa-arrow-right-from-bracket w-5"></i> ออกจากระบบ
                </button>
              </div>
            </div>
          </div>

          <router-link v-else to="/login" class="bg-white text-blue-900 hover:bg-blue-50 px-5 py-2 rounded-full text-sm font-bold transition-all shadow-lg hover:shadow-xl transform active:scale-95">
            เข้าสู่ระบบ
          </router-link>
        </div>
      </div>
    </div>

    <div
      v-if="showMobileMenu"
      class="md:hidden bg-[#1E3A8A]/95 backdrop-blur-xl border-t border-white/10 animate-fade-in-down"
    >
      <div class="px-6 py-4 flex flex-col gap-2">
        <router-link to="/" @click="showMobileMenu = false" class="px-4 py-3 rounded-lg text-blue-100 hover:bg-white/10 hover:text-white font-medium" active-class="bg-white/10 text-white font-bold">หน้าแรก</router-link>
        <router-link to="/category" @click="showMobileMenu = false" class="px-4 py-3 rounded-lg text-blue-100 hover:bg-white/10 hover:text-white font-medium" active-class="bg-white/10 text-white font-bold">หมวดหมู่</router-link>
        <router-link to="/news" @click="showMobileMenu = false" class="px-4 py-3 rounded-lg text-blue-100 hover:bg-white/10 hover:text-white font-medium" active-class="bg-white/10 text-white font-bold">ข่าวสาร</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import authService from '@/services/authService'
import notificationService from '@/services/notificationService'

const router = useRouter()
const route = useRoute()
const isLoggedIn = ref(false)
const showDropdown = ref(false)
const showMobileMenu = ref(false)
const showNotificationDropdown = ref(false)
const dropdownRef = ref(null)
const userProfile = ref(null)
const organizerStatus = ref('none')
const notifications = ref([])
const unreadCount = ref(0)

const fetchUserProfile = async () => {
  try {
    const response = await authService.getUserProfile()
    userProfile.value = response.data
    organizerStatus.value = response.data.organizer_status || 'none'
  } catch (error) {
    userProfile.value = null
  }
}

const fetchNotifications = async () => {
  try {
    const res = await notificationService.getMyNotifications()
    notifications.value = res.data.results || res.data || []
    unreadCount.value = notifications.value.filter(n => !n.is_read).length
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  }
}

const checkLoginStatus = () => {
  const token = localStorage.getItem("access")
  isLoggedIn.value = !!token
  
  if (isLoggedIn.value) {
    fetchUserProfile()
    fetchNotifications()
  } else {
    userProfile.value = null
    notifications.value = []
    unreadCount.value = 0
  }
}

const toggleNotificationDropdown = () => {
  showNotificationDropdown.value = !showNotificationDropdown.value
  if (showDropdown.value) showDropdown.value = false
}

const markAsRead = async (id) => {
  try {
    await notificationService.markAsRead(id)
    const notification = notifications.value.find(n => n.id === id)
    if (notification) notification.is_read = true
    unreadCount.value = notifications.value.filter(n => !n.is_read).length
  } catch (error) {
    console.error('Failed to mark as read:', error)
  }
}

const markAllAsRead = async () => {
  try {
    await notificationService.markAllRead()
    notifications.value.forEach(n => n.is_read = true)
    unreadCount.value = 0
  } catch (error) {
    console.error('Failed to mark all as read:', error)
  }
}

const formatNotificationDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)
  
  if (diff < 60) return 'เมื่อสักครู่'
  if (diff < 3600) return `${Math.floor(diff / 60)} นาทีที่แล้ว`
  if (diff < 86400) return `${Math.floor(diff / 3600)} ชั่วโมงที่แล้ว`
  if (diff < 604800) return `${Math.floor(diff / 86400)} วันที่แล้ว`
  return date.toLocaleDateString('th-TH', { day: 'numeric', month: 'short' })
}

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
  if (showNotificationDropdown.value) showNotificationDropdown.value = false
}

const closeDropdown = () => {
  showDropdown.value = false
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
  if (!event.target.closest('.relative')) {
    showNotificationDropdown.value = false
  }
}

const requestOrganizer = () => {
  router.push('/request-organizer')
  closeDropdown()
}

const handleLogout = () => {
  localStorage.removeItem("access")
  localStorage.removeItem("refresh")
  localStorage.removeItem("isAdmin")
  localStorage.removeItem("organizer_status")
  
  isLoggedIn.value = false
  userProfile.value = null
  closeDropdown()
  
  router.push('/login').then(() => {
    window.location.reload()
  })
}

onMounted(() => {
  checkLoginStatus()
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('storage', checkLoginStatus)
})

watch(() => route.path, () => {
  showMobileMenu.value = false
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('storage', checkLoginStatus)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.dropdown-item {
  @apply block px-5 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors flex items-center gap-3 cursor-pointer;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scale-in 0.15s ease-out;
}

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-down {
  animation: fade-in-down 0.2s ease-out;
}
</style>