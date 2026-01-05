<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F]">

    <Navbar />

    <main class="flex-grow container max-w-5xl mx-auto px-6 py-12 pt-32">
      
      <div class="mb-8">
        <router-link to="/news" class="inline-flex items-center gap-2 text-gray-500 hover:text-blue-600 transition font-medium bg-white border border-gray-200 px-5 py-2.5 rounded-full shadow-sm hover:shadow-md hover:-translate-x-1 duration-200">
          <i class="fa-solid fa-arrow-left-long text-sm"></i> 
          <span>กลับหน้ารวมข่าวสาร</span>
        </router-link>
      </div>

      <div v-if="isLoading" class="py-24 text-center">
        <div class="inline-block w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
        <p class="text-gray-500 font-medium">กำลังโหลดเนื้อหา...</p>
      </div>

      <div v-else-if="!news" class="py-24 text-center bg-white rounded-[32px] shadow-sm border border-gray-100 border-dashed">
        <div class="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4 text-red-400">
          <i class="fa-regular fa-circle-xmark text-4xl"></i>
        </div>
        <h2 class="text-xl font-bold text-gray-800 mb-2">ไม่พบข้อมูลข่าวสาร</h2>
        <p class="text-gray-500 text-sm mb-6">{{ errorMessage || 'ข่าวนี้อาจถูกลบหรือไม่มีอยู่ในระบบ' }}</p>
        <router-link to="/news" class="text-blue-600 font-bold hover:underline text-sm">กลับหน้าหลัก</router-link>
      </div>

      <article v-else class="bg-white rounded-[32px] shadow-xl overflow-hidden border border-gray-100 animate-fade-up">
        
        <div class="w-full h-[350px] md:h-[500px] relative bg-gray-100 group">
          <img 
            :src="news.image || 'https://via.placeholder.com/1200x600?text=News+Cover'" 
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-in-out"
            @error="(e) => e.target.src = 'https://via.placeholder.com/800x400?text=No+Image'"
            alt="News Cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#0F172A] via-[#0F172A]/40 to-transparent opacity-90"></div>
          
          <div class="absolute bottom-0 left-0 w-full p-8 md:p-12">
             <span class="bg-blue-600 text-white px-3 py-1 rounded-lg text-xs font-bold shadow-lg mb-4 inline-flex items-center gap-2 border border-white/20 backdrop-blur-md">
               <i class="fa-solid fa-bullhorn"></i> ข่าวประชาสัมพันธ์
             </span>
             <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold text-white leading-tight drop-shadow-md">
              {{ news.title }}
            </h1>
          </div>
        </div>

        <div class="px-8 md:px-12 py-10">
          <div class="flex flex-wrap items-center justify-between gap-6 pb-8 border-b border-gray-100 mb-8">
            <div class="flex items-center gap-6 text-gray-500 text-sm md:text-base font-medium">
              <div class="flex items-center gap-2">
                <i class="fa-regular fa-calendar-days text-blue-500 text-lg"></i>
                <span>{{ formatDate(news.created_at || news.publish_date) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <i class="fa-regular fa-user text-blue-500 text-lg"></i>
                <span>{{ news.author || 'Admin UEvent' }}</span>
              </div>
            </div>

            <button 
              @click="shareNews"
              class="flex items-center gap-2 text-blue-600 hover:text-white hover:bg-blue-600 px-5 py-2.5 rounded-full transition-all font-semibold bg-blue-50 shadow-sm border border-blue-100 hover:shadow-md active:scale-95"
            >
              <i class="fa-solid fa-share-nodes"></i> แชร์ข่าว
            </button>
          </div>

          <div class="prose prose-lg max-w-none text-gray-700 leading-loose whitespace-pre-line font-light">
            {{ news.detail || news.description || news.content }}
          </div>

        </div>
      </article>

      <div class="mt-12 text-center">
         <div class="w-16 h-1.5 bg-gray-200 mx-auto rounded-full mb-4"></div>
         <p class="text-gray-400 text-sm font-medium">สิ้นสุดเนื้อหาข่าว</p>
      </div>

    </main>

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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import newsService from '@/services/newsService.js'

const route = useRoute()
const router = useRouter()

const news = ref(null)
const isLoading = ref(true)
const isLoggedIn = ref(false)
const showDropdown = ref(false)
const errorMessage = ref('')

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem("access")
}

const handleLogout = () => {
  localStorage.removeItem("access")
  localStorage.removeItem("refresh")
  localStorage.removeItem("isAdmin")
  isLoggedIn.value = false
  showDropdown.value = false
  router.push("/")
}

const toggleDropdown = () => (showDropdown.value = !showDropdown.value)
const closeDropdown = () => (showDropdown.value = false)
const handleClickOutside = (e) => { if (!e.target.closest(".relative")) closeDropdown() }

// ⭐ Fetch News Detail Logic
const fetchNewsDetail = async () => {
  try {
    isLoading.value = true
    const newsId = route.params.id
    
    if (!newsId) throw new Error("News ID is missing")

    const response = await newsService.getNews(newsId)
    
    if (response.data) {
        news.value = response.data
    } else {
        throw new Error("No data returned from API")
    }

  } catch (error) {
    console.error("Error loading news detail:", error)
    errorMessage.value = error.response?.status === 404 
        ? "ไม่พบข่าวสารรหัสนี้ในระบบ (404)" 
        : "เกิดข้อผิดพลาดในการโหลดข้อมูล"
    news.value = null
  } finally {
    isLoading.value = false
  }
}

const formatDate = d => {
  if (!d) return '-'
  const date = new Date(d)
  const months = [
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
  ]
  return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear() + 543}`
}

const shareNews = () => {
  if (navigator.share) {
    navigator.share({
      title: news.value?.title || 'ข่าวสาร',
      url: window.location.href
    }).catch(console.error)
  } else {
    navigator.clipboard.writeText(window.location.href)
    alert("คัดลอกลิงก์ข่าวเรียบร้อยแล้ว")
  }
}

onMounted(() => {
  checkLoginStatus()
  fetchNewsDetail()
  document.addEventListener('click', handleClickOutside)
  window.scrollTo(0, 0)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-up { animation: fadeUp 0.6s ease-out; }
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scaleIn { 
  from { opacity: 0; transform: scale(0.95); } 
  to { opacity: 1; transform: scale(1); } 
}

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