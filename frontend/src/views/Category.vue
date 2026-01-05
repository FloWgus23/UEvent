<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F]">
    
    <div v-if="showToast" class="fixed top-24 left-1/2 -translate-x-1/2 z-50 pointer-events-none">
      <div :class="toastClass" class="px-6 py-3 rounded-full shadow-2xl text-white text-sm font-medium backdrop-blur-md bg-opacity-95 animate-fade-in-down pointer-events-auto flex items-center gap-2 border border-white/10">
        <i v-if="toastClass.includes('green')" class="fa-solid fa-check-circle"></i>
        <i v-else class="fa-solid fa-info-circle"></i>
        {{ toastMessage }}
      </div>
    </div>

    <Navbar />

    <div class="bg-white shadow-sm border-b border-gray-200 pt-28 pb-10">
      <div class="max-w-7xl mx-auto px-8 text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4 tracking-tight">หมวดหมู่กิจกรรม</h1>
        <p class="text-gray-500 text-lg font-light">เลือกหมวดหมู่ที่คุณสนใจเพื่อค้นหากิจกรรมที่ใช่สำหรับคุณ</p>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-8 py-12">

      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-12 animate-fade-up">
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="selectCategory(cat.id)"
          class="flex flex-col items-center justify-center p-4 rounded-2xl border transition-all duration-300 group aspect-square"
          :class="activeCategory === cat.id 
            ? 'bg-white border-blue-500 shadow-lg ring-4 ring-blue-50 transform scale-105' 
            : 'bg-white border-gray-100 hover:border-blue-200 hover:shadow-lg hover:-translate-y-1'"
        >
          <div 
            class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl mb-3 transition-colors shadow-sm"
            :class="activeCategory === cat.id ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' : 'bg-gray-50 text-gray-500 group-hover:bg-blue-50 group-hover:text-blue-600'"
          >
            <i :class="cat.icon"></i>
          </div>
          <span 
            class="font-semibold text-sm truncate w-full text-center px-1"
            :class="activeCategory === cat.id ? 'text-blue-700' : 'text-gray-600 group-hover:text-blue-700'"
          >
            {{ cat.name }}
          </span>
        </button>
      </div>

      <div class="flex items-center justify-between mb-8">
        <h2 class="text-2xl font-bold text-gray-800 flex items-center gap-3">
          <div class="w-1.5 h-8 bg-blue-600 rounded-full"></div>
          {{ activeCategoryName }}
        </h2>
        <span class="text-gray-500 text-sm font-medium bg-white border border-gray-200 px-3 py-1 rounded-full shadow-sm">{{ filteredActivities.length }} กิจกรรม</span>
      </div>

      <div v-if="isLoading" class="py-20 text-center">
        <div class="inline-block w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
        <p class="text-gray-500">กำลังโหลดกิจกรรม...</p>
      </div>

      <div v-else-if="filteredActivities.length === 0" class="py-24 text-center bg-white rounded-[32px] border border-dashed border-gray-200 shadow-sm">
        <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-300">
          <i class="fa-regular fa-folder-open text-3xl"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">ไม่พบกิจกรรมในหมวดหมู่นี้</h3>
        <p class="text-gray-500">ลองเลือกหมวดหมู่อื่นดูนะครับ</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="activity in filteredActivities"
          :key="activity.id"
          @click="$router.push(`/activity/${activity.id}`)"
          class="group bg-white rounded-[24px] shadow-[0_2px_12px_rgba(0,0,0,0.04)] hover:shadow-[0_12px_30px_rgba(30,58,138,0.12)] hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden border border-gray-100 flex flex-col h-full"
        >
          <div class="h-52 overflow-hidden relative bg-gray-100">
            <img 
              :src="activity.image || 'https://via.placeholder.com/400x200'" 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
              @error="(e) => e.target.src = 'https://via.placeholder.com/400x200'"
            />
            <div class="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-lg text-[11px] font-bold text-gray-900 shadow-sm border border-gray-100 uppercase tracking-wide">
              {{ getCategoryName(activity.category) }}
            </div>
          </div>

          <div class="p-6 flex flex-col flex-grow">
            <h3 class="text-lg font-bold text-gray-900 mb-3 line-clamp-2 leading-snug group-hover:text-blue-700 transition-colors">{{ activity.name }}</h3>
            
            <div class="space-y-2 text-sm text-gray-500 mb-6 flex-grow">
              <div class="flex items-center gap-3">
                <i class="fa-regular fa-calendar w-5 text-center text-blue-500"></i>
                <span>{{ formatDate(activity.date) }}</span>
              </div>
              <div class="flex items-center gap-3">
                <i class="fa-solid fa-location-dot w-5 text-center text-blue-500"></i>
                <span class="truncate">{{ activity.location }}</span>
              </div>
            </div>

            <div class="pt-5 border-t border-gray-50 mt-auto flex items-center justify-between">
              <span class="text-[11px] font-bold px-2.5 py-1 bg-gray-100 rounded-md text-gray-600 uppercase tracking-wide">
                {{ activity.organizer || 'UEvent' }}
              </span>
              <div class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center text-blue-500 group-hover:bg-blue-600 group-hover:text-white transition-all">
                <i class="fa-solid fa-arrow-right text-xs"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue"
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import activityService from '@/services/activityService'
import notificationService from "@/services/notificationService.js"
import OnboardingModal from "./OnboardingModal.vue" 

const router = useRouter()
const isLoading = ref(true)
const allActivities = ref([])
const activeCategory = ref('all')

// Navbar State
const isLoggedIn = ref(false)
const showDropdown = ref(false)
const showNotificationDropdown = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const showToast = ref(false)
const toastMessage = ref("")
const toastClass = ref("bg-[#1E3A8A]")

// 📌 Functions
const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem("access")
}

const handleLogout = () => {
  localStorage.clear()
  isLoggedIn.value = false
  showDropdown.value = false
  showNotificationDropdown.value = false
  router.push("/")
}

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
  if(showDropdown.value) showNotificationDropdown.value = false
}

const toggleNotificationDropdown = () => {
  showNotificationDropdown.value = !showNotificationDropdown.value
  if(showNotificationDropdown.value) showDropdown.value = false
}

const closeDropdown = () => {
  showDropdown.value = false
  showNotificationDropdown.value = false
}

const handleClickOutside = (e) => {
  if (!e.target.closest(".relative")) closeDropdown()
}

// Notification Logic
const fetchNotifications = async () => {
  if (!isLoggedIn.value) return
  try {
    const res = await notificationService.getMyNotifications()
    const data = Array.isArray(res.data) ? res.data : (res.data.results || [])
    notifications.value = data
    unreadCount.value = data.filter(n => !n.is_read).length
  } catch (e) {
    console.error("Noti error:", e)
  }
}

const handleReadNotification = async (item) => {
  if (!item.is_read) {
    try {
      await notificationService.markRead(item.id)
      item.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch(e) {}
  }
}

const markAllAsRead = async () => {
  try {
    await notificationService.markAllRead()
    notifications.value.forEach(n => n.is_read = true)
    unreadCount.value = 0
  } catch(e) {}
}

const deleteNotification = async (id) => {
  try {
    await notificationService.deleteNotification(id)
    notifications.value = notifications.value.filter(n => n.id !== id)
    unreadCount.value = notifications.value.filter(n => !n.is_read).length
  } catch(e) {}
}

const formatDateAgo = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)
  if (diff < 60) return 'เมื่อสักครู่'
  if (diff < 3600) return `${Math.floor(diff/60)} นาทีที่แล้ว`
  if (diff < 86400) return `${Math.floor(diff/3600)} ชั่วโมงที่แล้ว`
  return date.toLocaleDateString('th-TH')
}

// 📌 Category Data
const categories = [
  { id: 'all', name: 'ทั้งหมด', icon: 'fa-solid fa-layer-group' },
  { id: 'academic', name: 'วิชาการ', icon: 'fa-solid fa-graduation-cap' },
  { id: 'technology', name: 'เทคโนโลยี', icon: 'fa-solid fa-laptop-code' },
  { id: 'entertainment', name: 'บันเทิง', icon: 'fa-solid fa-masks-theater' },
  { id: 'sports', name: 'กีฬา', icon: 'fa-solid fa-futbol' },
  { id: 'volunteer', name: 'จิตอาสา', icon: 'fa-solid fa-hand-holding-heart' },
  { id: 'career', name: 'อาชีพ', icon: 'fa-solid fa-briefcase' },
]

const selectCategory = (id) => {
  activeCategory.value = id
}

const filteredActivities = computed(() => {
  if (activeCategory.value === 'all') {
    return allActivities.value
  }
  return allActivities.value.filter(act => act.category === activeCategory.value)
})

const activeCategoryName = computed(() => {
  const cat = categories.find(c => c.id === activeCategory.value)
  return cat ? (cat.id === 'all' ? 'กิจกรรมทั้งหมด' : `กิจกรรมหมวด${cat.name}`) : 'รายการกิจกรรม'
})

const getCategoryName = (id) => {
  const cat = categories.find(c => c.id === id)
  return cat ? cat.name : 'ทั่วไป'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: '2-digit' })
}

const fetchActivities = async () => {
  try {
    isLoading.value = true
    const res = await activityService.getAllActivities()
    // Handle Pagination format if needed
    const data = Array.isArray(res.data) ? res.data : (res.data.results || [])
    allActivities.value = data
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

// Lifecycle
onMounted(() => {
  checkLoginStatus()
  fetchActivities()
  if (isLoggedIn.value) {
    fetchNotifications()
    setInterval(fetchNotifications, 30000)
  }
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('storage', checkLoginStatus)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('storage', checkLoginStatus)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-up {
  animation: fadeUp 0.6s ease-out;
}

/* Dropdown Animation */
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

/* Scrollbar */
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  color: #1D1D1F;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  border-radius: 0.5rem;
  margin: 0 0.5rem;
}

.dropdown-item:hover {
  background-color: #F5F7FA;
}
</style>