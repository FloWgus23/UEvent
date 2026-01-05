<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F]">
    
    <Navbar />

    <div class="pt-28 pb-8 px-6 bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto">
         <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight flex items-center gap-3">
              <i class="fa-solid fa-chart-pie text-blue-600"></i>
              ภาพรวมสถิติ (Dashboard)
            </h1>
            <p class="text-gray-500 mt-2 ml-1">วิเคราะห์ข้อมูลกิจกรรมและสถิติการเข้าร่วมของคุณ</p>
          </div>
          
           <div class="flex gap-8">
             <div class="text-right px-6 border-r border-gray-200">
               <div class="text-4xl font-extrabold text-gray-900">{{ stats.completionRate }}%</div>
               <div class="text-xs text-gray-500 uppercase tracking-wide font-semibold mt-1">อัตราการเข้าร่วม</div>
             </div>
             <div class="text-right px-2">
               <div class="text-4xl font-extrabold text-blue-600">{{ stats.total }}</div>
               <div class="text-xs text-gray-500 uppercase tracking-wide font-semibold mt-1">กิจกรรมทั้งหมด</div>
             </div>
          </div>
        </div>
      </div>
    </div>

    <main class="flex-grow max-w-7xl mx-auto px-6 py-10 w-full">
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin h-10 w-10 border-4 border-blue-600 border-t-transparent rounded-full"></div>
        <p class="mt-4 text-gray-500 font-medium">กำลังประมวลผลข้อมูล...</p>
      </div>

      <div v-else class="space-y-8 animate-fade-in">
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2 bg-white rounded-[24px] p-8 shadow-[0_2px_12px_rgba(0,0,0,0.04)] border border-gray-100">
                <h3 class="font-bold text-gray-800 mb-6 flex items-center text-lg">
                    <span class="w-1.5 h-6 bg-blue-500 rounded-full mr-3"></span>
                    แนวโน้มกิจกรรมรายเดือน
                </h3>
                <div class="h-72 w-full">
                    <Bar v-if="monthlyChartData" :data="monthlyChartData" :options="chartOptions" />
                    <div v-else class="h-full flex items-center justify-center text-gray-400">ยังไม่มีข้อมูลกิจกรรม</div>
                </div>
            </div>

            <div class="lg:col-span-1 bg-white rounded-[24px] p-8 shadow-[0_2px_12px_rgba(0,0,0,0.04)] border border-gray-100">
                <h3 class="font-bold text-gray-800 mb-6 flex items-center text-lg">
                    <span class="w-1.5 h-6 bg-purple-500 rounded-full mr-3"></span>
                    สัดส่วนความสนใจ
                </h3>
                <div class="h-72 w-full flex items-center justify-center relative">
                    <Doughnut v-if="categoryChartData" :data="categoryChartData" :options="doughnutOptions" />
                    <div v-else class="text-gray-400 text-center">
                        <i class="fa-regular fa-chart-bar text-4xl mb-2 opacity-30 block"></i>
                        ยังไม่มีข้อมูล
                    </div>
                    
                    <div v-if="categoryChartData" class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                        <span class="text-4xl font-bold text-gray-900">{{ stats.total }}</span>
                        <span class="text-xs text-gray-500 uppercase tracking-widest mt-1">Total</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-[24px] p-6 shadow-lg shadow-blue-200 text-white transform hover:-translate-y-1 transition-transform duration-300">
             <div class="flex justify-between items-start">
                <div>
                    <p class="text-blue-100 text-sm font-medium mb-1">กิจกรรมถัดไป</p>
                    <h3 class="text-4xl font-bold">{{ stats.upcoming }}</h3>
                </div>
                <div class="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                    <i class="fa-solid fa-calendar-days text-2xl"></i>
                </div>
             </div>
             <p class="text-xs text-blue-100 mt-4 opacity-80 font-medium">รอเข้าร่วมเร็วๆ นี้</p>
          </div>

          <div class="bg-white rounded-[24px] p-6 shadow-sm border border-gray-100 flex justify-between items-center group hover:border-green-200 transition-colors">
             <div>
                <p class="text-gray-500 text-sm font-medium mb-1">เข้าร่วมสำเร็จ</p>
                <h3 class="text-4xl font-bold text-gray-900 group-hover:text-green-600 transition-colors">{{ stats.completed }}</h3>
                <p class="text-xs text-green-600 mt-1 flex items-center gap-1 font-medium bg-green-50 w-fit px-2 py-0.5 rounded-full">
                    <i class="fa-solid fa-check-circle"></i> เสร็จสิ้นแล้ว
                </p>
             </div>
             <div class="w-14 h-14 bg-green-50 rounded-full flex items-center justify-center text-green-500 text-2xl group-hover:scale-110 transition-transform">
                <i class="fa-solid fa-award"></i>
             </div>
          </div>

          <div class="bg-white rounded-[24px] p-6 shadow-sm border border-gray-100 flex justify-between items-center hover:border-orange-200 transition-colors">
             <div>
                <p class="text-gray-500 text-sm font-medium mb-1">กำลังรับสมัคร</p>
                <h3 class="text-4xl font-bold text-gray-900">{{ stats.registering }}</h3>
                 <p class="text-xs text-gray-400 mt-1">อยู่ในช่วงสมัคร</p>
             </div>
             <div class="w-14 h-14 bg-orange-50 rounded-full flex items-center justify-center text-orange-500 text-2xl">
                <i class="fa-solid fa-pen-to-square"></i>
             </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 overflow-hidden flex flex-col h-full">
               <div class="px-8 py-5 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                  <h3 class="font-bold text-gray-800 flex items-center gap-2 text-lg">
                      <i class="fa-solid fa-rocket text-blue-600"></i> ไฮไลท์กิจกรรม
                  </h3>
               </div>
               
               <div v-if="nextActivity" class="p-8 flex-grow flex flex-col">
                   <div class="relative w-full h-56 rounded-2xl overflow-hidden mb-6 group bg-gray-100 shadow-sm">
                       <img :src="nextActivity.activity.image || 'https://via.placeholder.com/600x300'" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                       <div class="absolute top-4 right-4 bg-white/95 backdrop-blur-md px-4 py-1.5 rounded-full text-xs font-bold text-blue-800 shadow-sm">
                          {{ formatDateShort(nextActivity.activity.date) }}
                       </div>
                   </div>
                   <h3 class="text-xl font-bold text-gray-900 mb-2 line-clamp-1">{{ nextActivity.activity.name }}</h3>
                   <div class="flex items-center text-sm text-gray-500 mb-6">
                       <i class="fa-solid fa-location-dot mr-2 text-red-500"></i> {{ nextActivity.activity.location }}
                   </div>
                   <router-link 
                      :to="`/activity/${nextActivity.activity.id}`"
                      class="mt-auto w-full block bg-[#1D1D1F] text-white text-center py-3.5 rounded-xl hover:bg-black transition-all font-medium shadow-lg active:scale-95"
                   >
                      ดูรายละเอียด
                   </router-link>
               </div>
               <div v-else class="p-12 text-center flex-grow flex flex-col justify-center items-center">
                   <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-4 text-gray-300">
                       <i class="fa-solid fa-coffee text-3xl"></i>
                   </div>
                   <p class="text-gray-400 font-medium">ไม่มีกิจกรรมเร็วๆ นี้</p>
               </div>
            </div>

            <div class="bg-white rounded-[24px] shadow-sm border border-gray-100 overflow-hidden flex flex-col h-full">
               <div class="px-8 py-5 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                  <h3 class="font-bold text-gray-800 text-lg">ไทม์ไลน์ล่าสุด</h3>
                  <router-link to="/profile/activities" class="text-xs font-bold text-blue-600 hover:text-blue-700 hover:underline">ดูทั้งหมด</router-link>
               </div>
               <div v-if="recentActivities.length > 0" class="divide-y divide-gray-50 overflow-y-auto max-h-[450px] custom-scrollbar">
                  <div v-for="reg in recentActivities" :key="reg.id" class="p-6 flex gap-5 hover:bg-gray-50/80 transition items-start group">
                     <div class="flex flex-col items-center">
                        <div class="w-3 h-3 rounded-full bg-blue-200 group-hover:bg-blue-500 transition-colors mt-2 ring-4 ring-blue-50"></div>
                        <div class="w-0.5 h-full bg-gray-100 mt-1"></div>
                     </div>
                     <div class="flex-1 pb-2">
                        <p class="text-xs font-semibold text-gray-400 mb-1 uppercase tracking-wide">{{ formatDate(reg.activity.date) }}</p>
                        <h4 class="text-base font-bold text-gray-900 line-clamp-1 mb-2 group-hover:text-blue-700 transition-colors">{{ reg.activity.name }}</h4>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-1 rounded-md text-[10px] bg-gray-100 text-gray-600 font-medium">
                                {{ getCategoryLabel(reg.activity.category) }}
                            </span>
                            <span class="text-[10px] font-bold" :class="getStatusClassText(reg.activity)">
                                {{ getStatusLabel(reg.activity) }}
                            </span>
                        </div>
                     </div>
                  </div>
               </div>
               <div v-else class="p-12 text-center flex-grow flex flex-col justify-center items-center text-gray-400">
                   <i class="fa-regular fa-folder-open text-3xl mb-3 opacity-30"></i>
                   ยังไม่มีประวัติการลงทะเบียน
               </div>
            </div>
        </div>

      </div>
    </main>

    <footer class="bg-gradient-to-r from-blue-900 via-blue-700 to-blue-900 text-white py-8 mt-auto">
      <div class="text-center">
         <div class="text-2xl font-bold opacity-90">UEvent</div>
         <div class="text-sm mt-2 opacity-60">© 2025 All Rights Reserved</div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue"
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import activityService from '@/services/activityService'

// Chart.js Imports
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
} from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title)

const router = useRouter()
const loading = ref(true)
const registrations = ref([])
const showDropdown = ref(false)

// Stats Data
const stats = ref({ total: 0, upcoming: 0, completed: 0, registering: 0, completionRate: 0 })

// Chart Config
const categoryLabels = {
    'academic': 'วิชาการ', 'technology': 'เทคโนโลยี', 'entertainment': 'บันเทิง',
    'sports': 'กีฬา', 'volunteer': 'จิตอาสา', 'career': 'อาชีพ', 'other': 'อื่นๆ'
}

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: { 
            backgroundColor: '#1e293b', 
            padding: 12, 
            cornerRadius: 12,
            titleFont: { family: 'Inter', size: 13 },
            bodyFont: { family: 'Inter', size: 12 }
        }
    },
    scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1, font: { family: 'Inter' } }, grid: { color: '#f1f5f9' }, border: { display: false } },
        x: { grid: { display: false }, ticks: { font: { family: 'Inter' } }, border: { display: false } }
    }
}

const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '75%',
    plugins: {
        legend: { 
            position: 'bottom', 
            labels: { usePointStyle: true, padding: 20, font: { size: 11, family: 'Inter' }, boxWidth: 8 } 
        }
    }
}

// ⭐ Main Fetch Function
const fetchData = async () => {
    try {
        // ใช้ URL ที่ถูกต้องจาก Service
        const response = await activityService.getMyRegistrations()
        // เก็บข้อมูล Registration (ซึ่งมี activity ซ้อนอยู่) ลงตัวแปร
        registrations.value = response.data
        
        console.log("Dashboard Data:", registrations.value) // Debug ดูข้อมูลได้
        calculateStats()
    } catch (error) {
        console.error("Error loading dashboard:", error)
        if (error.response?.status === 401) router.push('/login')
    } finally {
        loading.value = false
    }
}

const calculateStats = () => {
    const now = new Date()
    now.setHours(0,0,0,0)

    // นับจำนวนจาก registrations array
    stats.value.total = registrations.value.length
    
    // นับรายการที่ยังไม่ถึงกำหนด (Upcoming)
    stats.value.upcoming = registrations.value.filter(reg => {
        const actDate = new Date(reg.activity.date)
        actDate.setHours(0,0,0,0)
        return actDate >= now
    }).length
    
    // ที่เหลือคือเสร็จสิ้น (Completed/Past)
    stats.value.completed = stats.value.total - stats.value.upcoming
    
    // นับที่สถานะ activity เป็น 'กำลังรับสมัคร'
    stats.value.registering = registrations.value.filter(reg => reg.activity.status === 'กำลังรับสมัคร').length
    
    // Rate
    stats.value.completionRate = stats.value.total > 0 
        ? Math.round((stats.value.completed / stats.value.total) * 100) 
        : 0
}

// Chart Data (Computed)
const categoryChartData = computed(() => {
    if (registrations.value.length === 0) return null
    
    const counts = {}
    registrations.value.forEach(reg => {
        const cat = reg.activity.category
        counts[cat] = (counts[cat] || 0) + 1
    })

    return {
        labels: Object.keys(counts).map(k => categoryLabels[k] || k),
        datasets: [{
            backgroundColor: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#6366f1', '#9ca3af'],
            data: Object.values(counts),
            borderWidth: 0,
            hoverOffset: 4
        }]
    }
})

const monthlyChartData = computed(() => {
    if (registrations.value.length === 0) return null

    const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
    const monthlyCounts = new Array(12).fill(0)

    registrations.value.forEach(reg => {
        const date = new Date(reg.activity.date)
        if (!isNaN(date)) {
            monthlyCounts[date.getMonth()]++
        }
    })

    return {
        labels: months,
        datasets: [{
            label: 'จำนวนกิจกรรม',
            backgroundColor: '#3b82f6',
            borderRadius: 8,
            data: monthlyCounts,
            barThickness: 24,
            hoverBackgroundColor: '#2563eb'
        }]
    }
})

// Helpers for Template
const nextActivity = computed(() => {
    const now = new Date()
    now.setHours(0, 0, 0, 0)
    
    const upcoming = registrations.value
        .filter(reg => {
            const d = new Date(reg.activity.date)
            d.setHours(0,0,0,0)
            return d >= now
        })
        .sort((a, b) => new Date(a.activity.date) - new Date(b.activity.date))
        
    return upcoming.length > 0 ? upcoming[0] : null
})

const recentActivities = computed(() => {
    // เรียงตามวันที่ลงทะเบียนล่าสุด
    return [...registrations.value]
        .sort((a, b) => new Date(b.registered_at) - new Date(a.registered_at))
        .slice(0, 5)
})

const getCategoryLabel = (key) => categoryLabels[key] || key
const formatDate = (d) => d ? new Date(d).toLocaleDateString('th-TH', { year: 'numeric', month: 'short', day: 'numeric' }) : ''
const formatDateShort = (d) => d ? new Date(d).toLocaleDateString('th-TH', { month: 'short', day: 'numeric' }) : ''

const getStatusLabel = (act) => {
    const d = new Date(act.date)
    d.setHours(0,0,0,0)
    return d < new Date().setHours(0,0,0,0) ? 'จบแล้ว' : 'รอเข้าร่วม'
}
const getStatusClassText = (act) => {
    const d = new Date(act.date)
    d.setHours(0,0,0,0)
    return d < new Date().setHours(0,0,0,0) ? 'text-gray-400' : 'text-green-600'
}

const toggleDropdown = () => showDropdown.value = !showDropdown.value
const closeDropdown = () => showDropdown.value = false
const handleClickOutside = (e) => { if (!e.target.closest('.relative')) closeDropdown() }
const handleLogout = () => {
    localStorage.clear()
    router.push('/login')
}

onMounted(() => {
    fetchData()
    document.addEventListener('click', handleClickOutside)
})
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.font-sans {
    font-family: 'Inter', sans-serif;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

/* Scrollbar สวยๆ */
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