<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F]">

    <div v-if="showToast" class="fixed top-24 left-1/2 -translate-x-1/2 z-50 pointer-events-none">
      <div :class="{'bg-[#1E3A8A]': toastType === 'info', 'bg-green-600': toastType === 'success', 'bg-yellow-500': toastType === 'warning'}" class="px-6 py-3 rounded-full shadow-2xl text-white text-sm font-medium backdrop-blur-md bg-opacity-95 animate-fade-in-down pointer-events-auto flex items-center gap-2 border border-white/10">
        <i v-if="toastType === 'success'" class="fa-solid fa-check-circle"></i>
        <i v-else class="fa-solid fa-info-circle"></i>
        {{ toastMessage }}
      </div>
    </div>

    <Navbar />

    <div class="bg-white shadow-sm border-b border-gray-200 pt-32 pb-12">
      <div class="max-w-7xl mx-auto px-8 text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4 tracking-tight">
          <i class="fa-solid fa-newspaper text-blue-600 mr-2"></i> ข่าวสารและกิจกรรม
        </h1>
        <p class="text-gray-500 text-lg font-light">ติดตามข่าวสาร ประชาสัมพันธ์ และกิจกรรมต่างๆ ของมหาวิทยาลัย</p>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-8 py-16">

      <div v-if="isLoading" class="text-center py-20">
        <div class="inline-block w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
        <p class="text-gray-500 font-medium">กำลังโหลดข่าวสาร...</p>
      </div>

      <div v-else-if="newsList.length > 0" class="grid grid-cols-1 gap-10">
        
        <div
          v-for="news in newsList"
          :key="news.id"
          @click="handleNewsClick(news.id)"
          class="bg-white rounded-[24px] shadow-[0_4px_20px_rgba(0,0,0,0.03)] overflow-hidden hover:shadow-[0_12px_30px_rgba(30,58,138,0.1)] transition-all duration-300 transform hover:-translate-y-1 cursor-pointer group border border-gray-100"
        >
          <div class="flex flex-col md:flex-row h-full">
            <div class="md:w-2/5 h-64 md:h-auto overflow-hidden relative">
              <img
                :src="news.image"
                :alt="news.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                @error="handleImageError"
              />
              <div class="absolute top-4 left-4 bg-white/90 backdrop-blur-md text-blue-800 px-3 py-1.5 rounded-lg text-xs font-bold shadow-sm flex items-center gap-2">
                <div class="w-1.5 h-1.5 bg-blue-600 rounded-full"></div>
                ข่าวประชาสัมพันธ์
              </div>
            </div>

            <div class="flex-1 p-8 flex flex-col justify-between">
              <div>
                <h3 class="text-2xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors line-clamp-2 leading-tight">
                  {{ news.title }}
                </h3>
                <p class="text-gray-500 text-base leading-relaxed line-clamp-3 mb-6">
                  {{ news.description }}
                </p>
              </div>
              
              <div class="flex items-center justify-between mt-auto pt-5 border-t border-gray-50">
                <div class="flex items-center text-gray-400 text-sm font-medium">
                  <i class="fa-regular fa-calendar-check mr-2 text-blue-500"></i>
                  <span>{{ news.publishDate }}</span>
                </div>

                <div class="flex items-center gap-3">
                  <button 
                    @click.stop="shareNews(news)"
                    class="w-9 h-9 rounded-full bg-gray-50 text-gray-400 flex items-center justify-center hover:bg-blue-50 hover:text-blue-600 transition-colors border border-gray-100"
                    title="แชร์"
                  >
                    <i class="fa-solid fa-share-nodes text-sm"></i>
                  </button>
                  
                  <div class="flex items-center gap-1.5 text-blue-600 font-bold text-sm bg-blue-50 px-4 py-2 rounded-full group-hover:bg-blue-600 group-hover:text-white transition-all">
                    <span>อ่านต่อ</span>
                    <i class="fa-solid fa-arrow-right text-xs"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <div v-else class="text-center py-24 bg-white rounded-[32px] border border-dashed border-gray-200 shadow-sm">
        <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-300">
          <i class="fa-regular fa-newspaper text-3xl"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">ยังไม่มีข่าวสาร</h3>
        <p class="text-gray-500">ติดตามข่าวสารใหม่ๆ ได้เร็วๆ นี้</p>
      </div>
    </div>

    <footer class="bg-white border-t border-gray-200 py-12 mt-12">
      <div class="max-w-7xl mx-auto px-8 text-center">
        <div class="mb-4 flex justify-center items-center gap-2 text-gray-900 font-bold text-xl">
          <i class="fa-solid fa-calendar-star text-blue-600 text-2xl"></i>
          UEvent
        </div>
        <p class="text-gray-500 mb-8 max-w-md mx-auto text-sm leading-relaxed">
          แพลตฟอร์มบริหารจัดการกิจกรรมนักศึกษาที่ทันสมัย ใช้งานง่าย และตอบโจทย์ทุกไลฟ์สไตล์การเรียนรู้
        </p>
        <div class="text-xs text-gray-400">
          &copy; 2025 UEvent Project. All Rights Reserved.
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue"
import { ref, onMounted, onUnmounted, computed } from "vue"
import { useRouter } from "vue-router"
import newsService from "@/services/newsService.js"
import notificationService from "@/services/notificationService.js"

const router = useRouter()

const newsList = ref([])
const isLoggedIn = ref(false)
const isLoading = ref(false)
const showDropdown = ref(false)
const showNotificationDropdown = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const showToast = ref(false)
const toastMessage = ref("")
const toastType = ref("info")

/* ---------- Login Status ---------- */
const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem("access")
}

/* ---------- Logout ---------- */
const handleLogout = () => {
  localStorage.clear()
  isLoggedIn.value = false
  showDropdown.value = false
  router.push("/")
}

/* ---------- Dropdown ---------- */
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

/* ---------- Notification Logic ---------- */
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

/* ---------- Load News ---------- */
const fetchNews = async () => {
  try {
    isLoading.value = true
    const res = await newsService.getAllNews()
    const publishedNews = res.data.filter(n => n.status === "published")

    newsList.value = publishedNews.map(news => ({
      id: news.id,
      title: news.title,
      description: news.description || news.content,
      publishDate: formatDate(news.created_at || news.publish_date),
      image: news.image || "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400"
    }))

  } catch (error) {
    console.error("Error fetching news:", error)
  } finally {
    isLoading.value = false
  }
}

/* ---------- Format Date ---------- */
const formatDate = d => {
  if (!d) return '-'
  const date = new Date(d)
  const months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
  return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear() + 543}`
}

/* ---------- Toast Notification ---------- */
const triggerToast = (message, type = "info") => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 4000)
}

/* ---------- News Interaction ---------- */
const handleNewsClick = (id) => {
  router.push({ name: 'NewsDetail', params: { id: id } })
}

const shareNews = (news) => {
  if (navigator.share) {
    navigator.share({
      title: news.title,
      text: news.description,
      url: `${window.location.origin}/news/${news.id}`
    }).catch(console.error)
  } else {
    triggerToast("คัดลอกลิงก์เรียบร้อยแล้ว", "success")
    navigator.clipboard.writeText(`${window.location.origin}/news/${news.id}`)
  }
}

const handleImageError = (e) => {
  e.target.src = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400"
}

/* ---------- Lifecycle ---------- */
onMounted(() => {
  checkLoginStatus()
  fetchNews()
  if (isLoggedIn.value) {
    fetchNotifications()
    setInterval(fetchNotifications, 30000)
  }
  window.addEventListener("storage", checkLoginStatus)
  document.addEventListener("click", handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener("storage", checkLoginStatus)
  document.removeEventListener("click", handleClickOutside)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.animate-fade-in-down { animation: fadeInDown 0.2s ease-out; }
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }

@keyframes fadeInDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
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
.dropdown-item:hover { background-color: #F5F7FA; }
</style>