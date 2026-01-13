<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900">
    
    <header class="bg-blue-900/50 backdrop-blur-sm shadow-lg sticky top-0 z-50 border-b border-white/10">
      <div class="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
        <h1 class="text-white text-3xl font-bold flex items-center gap-3">
          UEvent <span class="text-sm font-normal opacity-70 bg-blue-700 px-2 py-1 rounded-md">Organizer</span>
        </h1>

        <div class="flex items-center gap-6">
          <button @click="router.push('/')" class="text-blue-100 hover:text-white transition-colors text-sm font-medium flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-white/10">
            <i class="fa-solid fa-home"></i> หน้าแรกเว็บไซต์
          </button>

          <div class="relative">
            <button @click="toggleDropdown" class="w-10 h-10 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition shadow-md border-2 border-blue-200 overflow-hidden">
              <!-- ⭐ แสดงรูปโปรไฟล์ถ้ามี -->
              <img 
                v-if="userProfile?.profile?.profile_image" 
                :src="userProfile.profile.profile_image" 
                alt="Profile"
                class="w-full h-full object-cover"
              />
              <i v-else class="fa-solid fa-user text-blue-900"></i>
            </button>
            <div v-if="showDropdown" class="absolute right-0 mt-3 w-56 bg-white text-gray-800 rounded-xl shadow-2xl py-2 z-50 border border-gray-100 transform origin-top-right transition-all">
              <div class="px-4 py-3 border-b border-gray-100">
                <p class="text-sm font-bold text-gray-900">ผู้จัดกิจกรรม</p>
              </div>
              <router-link to="/profile" class="block px-4 py-3 hover:bg-blue-50 text-sm transition-colors" @click="closeDropdown">
                <i class="fa-solid fa-id-card mr-2 text-blue-500"></i> โปรไฟล์
              </router-link>
              <button class="w-full text-left px-4 py-3 text-red-600 hover:bg-red-50 text-sm transition-colors" @click="handleLogout">
                <i class="fa-solid fa-right-from-bracket mr-2"></i> ออกจากระบบ
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <div class="bg-white rounded-[2rem] shadow-xl p-8 min-h-[85vh]">
        
        <div class="flex flex-wrap gap-4 mb-8">
          <button @click="activeTab = 'dashboard'" :class="getTabClass('dashboard')">
            <i class="fa-solid fa-chart-pie mr-2"></i> แดชบอร์ด
          </button>
          <button @click="activeTab = 'create'" :class="getTabClass('create')">
            <i class="fa-solid fa-plus-circle mr-2"></i> สร้างกิจกรรม/ข่าว
          </button>
          <button @click="switchToManageTab" :class="getTabClass('home')">
            <i class="fa-solid fa-list-check mr-2"></i> จัดการข้อมูล
          </button>
        </div>

        <div class="w-full h-px bg-gray-100 mb-8"></div>

        <div v-if="activeTab === 'dashboard'" class="animate-fade-in">
          
          <div class="flex flex-col md:flex-row justify-between items-end mb-8 gap-4">
            <div>
              <h2 class="text-3xl font-bold text-gray-800">ภาพรวมระบบ</h2>
              <p class="text-gray-500 mt-1">สถิติและข้อมูลสำคัญสำหรับผู้จัดงาน</p>
            </div>
            <div class="flex gap-3">
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow relative overflow-hidden group">
              <div class="flex justify-between items-start z-10 relative">
                <div>
                  <p class="text-blue-100 text-sm font-medium">กิจกรรมทั้งหมด</p>
                  <h3 class="text-4xl font-bold mt-2">{{ dashboardStats.totalEvents }}</h3>
                </div>
                <div class="p-3 bg-white/20 rounded-lg backdrop-blur-sm">
                  <i class="fa-solid fa-calendar-check text-2xl"></i>
                </div>
              </div>
              <i class="fa-solid fa-calendar-days absolute -bottom-4 -right-4 text-8xl opacity-10 transform -rotate-12 group-hover:scale-110 transition-transform"></i>
            </div>

            <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow relative overflow-hidden group">
              <div class="flex justify-between items-start z-10 relative">
                <div>
                  <p class="text-purple-100 text-sm font-medium">ผู้ลงทะเบียนรวม</p>
                  <h3 class="text-4xl font-bold mt-2">{{ dashboardStats.totalRegistrations }}</h3>
                </div>
                <div class="p-3 bg-white/20 rounded-lg backdrop-blur-sm">
                  <i class="fa-solid fa-users text-2xl"></i>
                </div>
              </div>
               <i class="fa-solid fa-users-viewfinder absolute -bottom-4 -right-4 text-8xl opacity-10 transform -rotate-12 group-hover:scale-110 transition-transform"></i>
            </div>

            <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow relative overflow-hidden group">
              <div class="flex justify-between items-start z-10 relative">
                <div>
                  <p class="text-green-100 text-sm font-medium">กำลังเปิดรับสมัคร</p>
                  <h3 class="text-4xl font-bold mt-2">{{ dashboardStats.activeEvents }}</h3>
                </div>
                <div class="p-3 bg-white/20 rounded-lg backdrop-blur-sm">
                  <i class="fa-solid fa-clock text-2xl"></i>
                </div>
              </div>
              <i class="fa-solid fa-stopwatch absolute -bottom-4 -right-4 text-8xl opacity-10 transform -rotate-12 group-hover:scale-110 transition-transform"></i>
            </div>

            <div class="bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow relative overflow-hidden group">
              <div class="flex justify-between items-start z-10 relative">
                <div>
                  <p class="text-orange-100 text-sm font-medium">ข่าวสารที่เผยแพร่</p>
                  <h3 class="text-4xl font-bold mt-2">{{ dashboardStats.totalNews }}</h3>
                </div>
                <div class="p-3 bg-white/20 rounded-lg backdrop-blur-sm">
                  <i class="fa-solid fa-newspaper text-2xl"></i>
                </div>
              </div>
              <i class="fa-solid fa-bullhorn absolute -bottom-4 -right-4 text-8xl opacity-10 transform -rotate-12 group-hover:scale-110 transition-transform"></i>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            <div class="lg:col-span-2 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
              <div class="flex justify-between items-center mb-6">
                 <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                   <div class="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center text-blue-600">
                     <i class="fa-solid fa-chart-line"></i>
                   </div>
                   แนวโน้มการลงทะเบียน
                 </h3>
              </div>
              <div class="h-72 relative">
                 <Line :data="chartData.registrationTrend" :options="lineChartOptions" />
              </div>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex flex-col">
              <h3 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
                <div class="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center text-purple-600">
                  <i class="fa-solid fa-chart-pie"></i>
                </div>
                สัดส่วนตามคณะ
              </h3>
              <div class="h-56 relative flex justify-center items-center">
                 <Doughnut :data="chartData.demographics" :options="doughnutOptions" />
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mb-12">
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                <div class="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center text-green-600">
                  <i class="fa-solid fa-calendar-day"></i>
                </div>
                กำหนดการเร็วๆ นี้
              </h3>
            </div>
            
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="(event, index) in upcomingEvents" :key="index" class="flex gap-4 items-start group p-4 rounded-xl border border-gray-100 hover:border-blue-200 hover:bg-blue-50 transition-all cursor-default shadow-sm hover:shadow-md bg-white">
                  <div class="flex-shrink-0 w-14 h-14 bg-blue-50 rounded-xl flex flex-col items-center justify-center text-blue-700 border border-blue-100 group-hover:bg-blue-600 group-hover:text-white transition-colors shadow-sm">
                    <span class="text-xs font-bold uppercase">{{ event.month }}</span>
                    <span class="text-xl font-bold">{{ event.day }}</span>
                  </div>
                  <div class="flex-grow pt-1 overflow-hidden">
                    <h4 class="font-bold text-gray-800 group-hover:text-blue-600 transition-colors truncate">{{ event.name }}</h4>
                    <div class="flex flex-col gap-1 text-sm text-gray-500 mt-2">
                      <span class="flex items-center gap-2"><i class="fa-regular fa-clock text-xs w-4"></i> {{ event.time }}</span>
                      <span class="flex items-center gap-2 truncate"><i class="fa-solid fa-location-dot text-xs w-4"></i> {{ event.location }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="upcomingEvents.length === 0" class="text-center text-gray-500 py-8 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                <i class="fa-regular fa-calendar-xmark text-4xl mb-2 text-gray-400"></i>
                <p>ยังไม่มีกิจกรรมที่กำลังจะมาถึง</p>
              </div>
            </div>
          </div>

        </div>

        <div v-else-if="activeTab === 'home'" class="animate-fade-in">
           <div class="mb-12">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800 border-l-4 border-blue-500 pl-3">จัดการกิจกรรม</h2>
              <button @click="router.push('/organizer/create-activity')" class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition shadow-lg shadow-blue-200 flex items-center gap-2">
                <i class="fa-solid fa-plus"></i> เพิ่มกิจกรรม
              </button>
            </div>
            
            <div class="overflow-x-auto bg-white rounded-xl border border-gray-200 shadow-sm">
              <table class="w-full">
                <thead class="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">ชื่อกิจกรรม</th>
                    <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">วันที่จัด</th>
                    <th class="px-6 py-4 text-center text-sm font-semibold text-gray-600">ผู้ลงทะเบียน</th>
                    <th class="px-6 py-4 text-center text-sm font-semibold text-gray-600">สถานะ</th>
                    <th class="px-6 py-4 text-center text-sm font-semibold text-gray-600">เครื่องมือ</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                   <tr v-if="isLoading">
                     <td colspan="5" class="text-center py-8 text-gray-500">กำลังโหลดข้อมูล...</td>
                   </tr>
                   <tr v-else-if="activities.length === 0">
                      <td colspan="5" class="text-center py-8 text-gray-500">ยังไม่มีข้อมูลกิจกรรม</td>
                   </tr>
                   <tr v-for="activity in paginatedActivities" :key="activity.id" class="hover:bg-blue-50/30 transition-colors">
                     <td class="px-6 py-4 font-medium text-gray-900">{{ activity.name }}</td>
                     <td class="px-6 py-4 text-gray-600">{{ activity.date }}</td>
                     <td class="px-6 py-4 text-center">
                       <span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-bold border border-gray-200">{{ activity.registered }}</span>
                     </td>
                     <td class="px-6 py-4 text-center">
                       <span :class="getStatusClass(activity.status)">{{ activity.status }}</span>
                     </td>
                     <td class="px-6 py-4 text-center">
                       <div class="flex justify-center gap-2">
                          <button @click="viewRegistrations(activity.id)" class="w-9 h-9 rounded-lg border border-blue-200 text-blue-600 hover:bg-blue-50 flex items-center justify-center transition" title="รายชื่อ">
                            <i class="fa-solid fa-users text-sm"></i>
                          </button>
                          <button @click="editActivity(activity.id)" class="w-9 h-9 rounded-lg border border-yellow-200 text-yellow-600 hover:bg-yellow-50 flex items-center justify-center transition" title="แก้ไข">
                            <i class="fa-solid fa-pen text-sm"></i>
                          </button>
                          <button @click="deleteActivity(activity.id)" class="w-9 h-9 rounded-lg border border-red-200 text-red-600 hover:bg-red-50 flex items-center justify-center transition" title="ลบ">
                            <i class="fa-solid fa-trash text-sm"></i>
                          </button>
                       </div>
                     </td>
                   </tr>
                </tbody>
              </table>
            </div>
             <div class="flex justify-end items-center gap-2 mt-4" v-if="totalPages > 1">
              <button class="px-3 py-1 rounded border hover:bg-gray-50 disabled:opacity-50" :disabled="currentPage === 1" @click="prevPage"><</button>
              <span class="text-sm text-gray-600">หน้า {{ currentPage }} / {{ totalPages }}</span>
              <button class="px-3 py-1 rounded border hover:bg-gray-50 disabled:opacity-50" :disabled="currentPage === totalPages" @click="nextPage">></button>
            </div>
          </div>

          <div class="mt-12">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800 border-l-4 border-green-500 pl-3">จัดการข่าวสาร</h2>
              <button @click="createNews" class="px-5 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 transition shadow-lg shadow-green-200 flex items-center gap-2">
                <i class="fa-solid fa-bullhorn"></i> เพิ่มข่าวสาร
              </button>
            </div>
             <div class="overflow-x-auto bg-white rounded-xl border border-gray-200 shadow-sm">
               <table class="w-full">
                 <thead class="bg-gray-50 border-b border-gray-200">
                   <tr>
                     <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600 w-2/5">หัวข้อข่าว</th>
                     <th class="px-6 py-4 text-center text-sm font-semibold text-gray-600 w-1/5">วันที่</th>
                     <th class="px-6 py-4 text-center text-sm font-semibold text-gray-600 w-1/5">สถานะ</th>
                     <th class="px-6 py-4 text-center text-sm font-semibold text-gray-600 w-1/5">เครื่องมือ</th>
                   </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                     <tr v-if="newsList.length === 0">
                        <td colspan="4" class="text-center py-8 text-gray-500">ยังไม่มีข้อมูลข่าวสาร</td>
                     </tr>
                     <tr v-for="news in paginatedNews" :key="news.id" class="hover:bg-green-50/30 transition-colors">
                       <td class="px-6 py-4 font-medium text-gray-900">{{ news.title }}</td>
                       <td class="px-6 py-4 text-gray-600 text-center">{{ news.publishDate || '-' }}</td>
                       <td class="px-6 py-4 text-center">
                          <span :class="getNewsStatusClass(news.statusRaw)">
                            {{ news.statusDisplay }}
                          </span>
                       </td>
                       <td class="px-6 py-4 text-center">
                         <div class="flex justify-center gap-3">
                            <button @click="viewNews(news.id)" class="text-gray-400 hover:text-blue-600 transition" title="ดูตัวอย่าง">
                               <i class="fa-solid fa-eye"></i>
                            </button>
                            <button @click="editNews(news.id)" class="text-gray-400 hover:text-yellow-600 transition" title="แก้ไข">
                               <i class="fa-solid fa-pen"></i>
                            </button>
                            <button @click="deleteNews(news.id)" class="text-red-500 hover:text-red-700 transition" title="ลบ">
                               <i class="fa-solid fa-trash"></i>
                            </button>
                         </div>
                       </td>
                     </tr>
                  </tbody>
               </table>
             </div>
             <div class="flex justify-end items-center gap-2 mt-4" v-if="newsTotalPages > 1">
              <button class="px-3 py-1 rounded border hover:bg-gray-50 disabled:opacity-50" :disabled="newsCurrentPage === 1" @click="prevNewsPage"><</button>
              <span class="text-sm text-gray-600">หน้า {{ newsCurrentPage }} / {{ newsTotalPages }}</span>
              <button class="px-3 py-1 rounded border hover:bg-gray-50 disabled:opacity-50" :disabled="newsCurrentPage === newsTotalPages" @click="nextNewsPage">></button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'create'" class="py-12 animate-fade-in">
          <div class="max-w-4xl mx-auto">
            <h2 class="text-3xl font-bold text-gray-800 text-center mb-12">เลือกประเภทสิ่งที่ต้องการสร้าง</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl mx-auto">
              <div @click="router.push('/organizer/create-activity')" class="group bg-white rounded-3xl p-8 border-2 border-blue-100 hover:border-blue-500 cursor-pointer shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative overflow-hidden">
                <div class="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
                   <i class="fa-solid fa-calendar-plus text-9xl text-blue-600"></i>
                </div>
                <div class="flex flex-col items-center text-center space-y-6 relative z-10">
                  <div class="w-24 h-24 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <i class="fa-solid fa-calendar-plus text-4xl text-white"></i>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-gray-800 group-hover:text-blue-600 transition">สร้างกิจกรรมใหม่</h3>
                    <p class="text-gray-500 mt-2">สำหรับงานอีเวนต์ อบรม หรือกิจกรรมนักศึกษา พร้อมระบบลงทะเบียน</p>
                  </div>
                  <button class="px-8 py-3 bg-blue-600 text-white rounded-xl shadow-lg hover:bg-blue-700 transition w-full font-semibold">เริ่มสร้าง</button>
                </div>
              </div>

              <div @click="createNews" class="group bg-white rounded-3xl p-8 border-2 border-green-100 hover:border-green-500 cursor-pointer shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative overflow-hidden">
                 <div class="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
                   <i class="fa-solid fa-bullhorn text-9xl text-green-600"></i>
                </div>
                 <div class="flex flex-col items-center text-center space-y-6 relative z-10">
                  <div class="w-24 h-24 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <i class="fa-solid fa-bullhorn text-4xl text-white"></i>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-gray-800 group-hover:text-green-600 transition">ประกาศข่าวสาร</h3>
                    <p class="text-gray-500 mt-2">แจ้งเตือนข่าวสาร ประชาสัมพันธ์ หรือการเปลี่ยนแปลงกำหนดการ</p>
                  </div>
                  <button class="px-8 py-3 bg-green-600 text-white rounded-xl shadow-lg hover:bg-green-700 transition w-full font-semibold">เขียนข่าว</button>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div v-if="showPreview" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in" @click.self="closePreview">
      <div class="bg-white w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h3 class="text-xl font-bold text-gray-800">ตัวอย่างข่าวสาร</h3>
          <button @click="closePreview" class="w-8 h-8 rounded-full bg-white text-gray-500 hover:bg-red-50 hover:text-red-500 transition shadow-sm flex items-center justify-center">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
        <div class="p-8 overflow-y-auto">
          <span :class="getNewsStatusClass(selectedNews.statusRaw)" class="mb-4">{{ selectedNews.statusDisplay }}</span>
          <h2 class="text-2xl font-bold text-gray-900 mb-2 mt-3">{{ selectedNews.title }}</h2>
          <div class="text-sm text-gray-500 mb-6 flex items-center gap-2">
            <i class="fa-regular fa-calendar"></i> {{ selectedNews.publishDate || '-' }}
          </div>
          <div class="prose max-w-none text-gray-600">
            <p v-if="selectedNews.content">{{ selectedNews.content }}</p>
            <p v-else class="text-gray-400 italic text-center py-8">-- ไม่พบเนื้อหาข่าวฉบับเต็ม --</p>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-end gap-3">
          <button @click="closePreview" class="px-4 py-2 text-gray-600 hover:bg-gray-200 rounded-lg transition">ปิดหน้าต่าง</button>
          <button @click="editNews(selectedNews.id)" class="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition shadow-md shadow-yellow-200">
            <i class="fa-solid fa-pen mr-1"></i> แก้ไขข่าวนี
          </button>
        </div>
      </div>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement
} from 'chart.js'
import { Bar, Line, Doughnut } from 'vue-chartjs'
import apiClient from '@/services/api.js'
import activityService from '@/services/activityService.js'
import newsService from '@/services/newsService.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement, ArcElement)

const router = useRouter()
const activeTab = ref('dashboard')

// Dropdown & Logout
const showDropdown = ref(false)
const userProfile = ref(null)
const toggleDropdown = () => (showDropdown.value = !showDropdown.value)
const closeDropdown = () => (showDropdown.value = false)
const handleLogout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('isAdmin')
  localStorage.removeItem('organizer_status')
  router.push('/')
}
const handleClickOutside = (e) => { if (!e.target.closest('.relative')) closeDropdown() }

// Utility
const getTabClass = (tabName) => {
  const base = "px-6 py-3 rounded-xl font-bold transition-all flex items-center shadow-sm"
  return activeTab.value === tabName
    ? `${base} bg-blue-600 text-white shadow-blue-300/50 hover:bg-blue-700 transform scale-105`
    : `${base} bg-white text-gray-600 border border-gray-200 hover:bg-gray-50 hover:text-blue-600`
}

const getStatusClass = (status) => {
  const base = "px-3 py-1 rounded-full text-xs font-semibold border"
  if (status === 'กำลังรับสมัคร') return `${base} bg-blue-100 text-blue-700 border-blue-200`
  if (status === 'กำลังดำเนินการ') return `${base} bg-green-100 text-green-700 border-green-200`
  return `${base} bg-red-100 text-red-700 border-red-200`
}

const getNewsStatusClass = (statusRaw) => {
  const base = "px-3 py-1 rounded-full text-xs font-semibold border inline-block min-w-[80px]";
  if (statusRaw === 'published') return `${base} bg-green-100 text-green-700 border-green-200`;
  return `${base} bg-gray-100 text-gray-600 border-gray-200`;
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  if (Number.isNaN(date.getTime())) return '-'
  const m = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
  return `${date.getDate()} ${m[date.getMonth()]} ${date.getFullYear() + 543}`
}

/* ================= DATA & CHARTS ================= */
const dashboardStats = ref({ totalEvents: 0, totalRegistrations: 0, activeEvents: 0, totalNews: 0 })
const upcomingEvents = ref([])

// ⭐ แก้ไขให้ดึงข้อมูลจาก Backend
const chartData = ref({
  popularEvents: { 
    labels: [], 
    datasets: [{ 
      label: 'ผู้ลงทะเบียน', 
      backgroundColor: '#3B82F6', 
      borderRadius: 6, 
      data: [] 
    }] 
  },
  registrationTrend: { 
    labels: ['กำลังโหลด...'], 
    datasets: [{ 
      label: 'ยอดลงทะเบียนใหม่', 
      borderColor: '#8B5CF6', 
      backgroundColor: 'rgba(139, 92, 246, 0.1)', 
      borderWidth: 3, 
      pointBackgroundColor: '#ffffff', 
      pointBorderColor: '#8B5CF6',
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: true, 
      tension: 0.4, 
      data: [0] 
    }] 
  },
  demographics: { 
    labels: ['กำลังโหลด...'], 
    datasets: [{ 
      backgroundColor: ['#E5E7EB'], 
      borderWidth: 0, 
      data: [1] 
    }] 
  }
})

const barChartOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { borderDash: [2, 4] } }, x: { grid: { display: false } } } }
const lineChartOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { borderDash: [2, 4] } }, x: { grid: { display: false } } } }
const doughnutOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, cutout: '70%' }

/* ================= API CALLS ================= */
const activities = ref([])
const newsList = ref([])
const isLoading = ref(false)

// Pagination
const itemsPerPage = 8
const currentPage = ref(1)
const totalPages = computed(() => Math.ceil(activities.value.length / itemsPerPage || 1))
const paginatedActivities = computed(() => activities.value.slice((currentPage.value - 1) * itemsPerPage, currentPage.value * itemsPerPage))
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }

const newsItemsPerPage = 5
const newsCurrentPage = ref(1)
const newsTotalPages = computed(() => Math.ceil(newsList.value.length / newsItemsPerPage || 1))
const paginatedNews = computed(() => newsList.value.slice((newsCurrentPage.value - 1) * newsItemsPerPage, newsCurrentPage.value * newsItemsPerPage))
const nextNewsPage = () => { if (newsCurrentPage.value < newsTotalPages.value) newsCurrentPage.value++ }
const prevNewsPage = () => { if (newsCurrentPage.value > 1) newsCurrentPage.value-- }

const showPreview = ref(false)
const selectedNews = ref({})

const updateCharts = () => {
  if (activities.value.length === 0) return
  const sortedActivities = [...activities.value].sort((a, b) => (parseInt(b.registered) || 0) - (parseInt(a.registered) || 0)).slice(0, 5)
  chartData.value.popularEvents = {
    labels: sortedActivities.map(a => a.name),
    datasets: [{ label: 'ผู้ลงทะเบียน', backgroundColor: '#3B82F6', borderRadius: 6, data: sortedActivities.map(a => parseInt(a.registered) || 0) }]
  }
}

const updateUpcomingEvents = (allActivities) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const sorted = allActivities.filter(a => new Date(a.date) >= today).sort((a, b) => new Date(a.date) - new Date(b.date)).slice(0, 3)
  const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
  upcomingEvents.value = sorted.map(a => {
    const d = new Date(a.date)
    return { id: a.id, name: a.name, month: months[d.getMonth()], day: d.getDate(), time: a.time_display || '09:00 - 16:00', location: a.location || 'ไม่ระบุสถานที่' }
  })
}

const fetchActivities = async () => {
  try {
    isLoading.value = true
    const res = await activityService.getMyActivities()
    
    const rawData = Array.isArray(res.data) ? res.data : (res.data.results || [])
    
    activities.value = rawData.map(a => ({ 
      id: a.id, 
      name: a.name, 
      date: formatDate(a.date), 
      registered: a.registered_count || 0, 
      status: a.status, 
      rawDate: a.date, 
      time_display: a.time_display, 
      location: a.location,
      image: a.image
    }))
    
    if (activities.value.length) {
      dashboardStats.value.totalEvents = activities.value.length
      dashboardStats.value.totalRegistrations = activities.value.reduce((acc, curr) => acc + (parseInt(curr.registered) || 0), 0)
      dashboardStats.value.activeEvents = activities.value.filter(a => a.status === 'กำลังรับสมัคร').length
      updateCharts()
      updateUpcomingEvents(rawData)
    }
  } catch (error) {
    console.error("Error loading activities:", error)
  } finally { 
    isLoading.value = false 
  }
}

const fetchNews = async () => {
  try {
    const res = await newsService.getMyNews()
    const rawData = Array.isArray(res.data) ? res.data : (res.data.results || [])
    
    newsList.value = rawData.map(n => ({ 
      id: n.id, 
      title: n.title, 
      publishDate: n.publish_date ? formatDate(n.publish_date) : null,
      statusRaw: n.status,
      statusDisplay: n.status === 'published' ? 'เผยแพร่แล้ว' : 'ฉบับร่าง',
      content: n.detail || n.content || ''
    }))
    if (newsList.value.length) dashboardStats.value.totalNews = newsList.value.length
  } catch (e) { console.error(e) }
}

// ⭐ เพิ่มฟังก์ชันดึงสถิติจาก Backend
const fetchFacultyStatistics = async () => {
  try {
    const response = await apiClient.get('/statistics/faculty/')
    const { labels, data } = response.data
    
    if (labels && data && labels.length > 0) {
      const colors = [
        '#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', 
        '#EF4444', '#EC4899', '#6366F1', '#14B8A6'
      ]
      
      const backgroundColor = labels.map((_, index) => colors[index % colors.length])
      
      chartData.value.demographics = {
        labels: labels,
        datasets: [{
          backgroundColor: backgroundColor,
          borderWidth: 0,
          data: data
        }]
      }
      
      console.log('✅ Faculty statistics loaded:', { labels, data })
    }
  } catch (error) {
    console.error('❌ Error loading faculty statistics:', error)
    chartData.value.demographics = {
      labels: ['ไม่มีข้อมูล'],
      datasets: [{
        backgroundColor: ['#E5E7EB'],
        borderWidth: 0,
        data: [1]
      }]
    }
  }
}

const fetchRegistrationTrend = async () => {
  try {
    const response = await apiClient.get('/statistics/registration-trend/')
    const { labels, data } = response.data
    
    if (labels && data) {
      chartData.value.registrationTrend = {
        labels: labels,
        datasets: [{
          label: 'ยอดลงทะเบียนใหม่',
          borderColor: '#8B5CF6',
          backgroundColor: 'rgba(139, 92, 246, 0.1)',
          borderWidth: 3,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#8B5CF6',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          fill: true,
          tension: 0.4,
          data: data
        }]
      }
      
      console.log('✅ Registration trend loaded:', { labels, data })
    }
  } catch (error) {
    console.error('❌ Error loading registration trend:', error)
    chartData.value.registrationTrend = {
      labels: ['จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.', 'อา.'],
      datasets: [{
        label: 'ยอดลงทะเบียนใหม่',
        borderColor: '#8B5CF6',
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: '#ffffff',
        pointBorderColor: '#8B5CF6',
        fill: true,
        tension: 0.4,
        data: [0, 0, 0, 0, 0, 0, 0]
      }]
    }
  }
}

const viewRegistrations = (id) => router.push(`/organizer/activity/${id}/registrations`)
const editActivity = (id) => router.push(`/organizer/edit-activity/${id}`)
const deleteActivity = async (id) => { if (confirm('ลบกิจกรรม?')) { await activityService.deleteActivity(id); fetchActivities() } }

const viewNews = (id) => {
  const newsItem = newsList.value.find(n => n.id === id)
  if (newsItem) {
    selectedNews.value = newsItem
    showPreview.value = true
  }
}
const closePreview = () => { showPreview.value = false; selectedNews.value = {} }
const editNews = (id) => router.push(`/organizer/edit-news/${id}`)
const deleteNews = async (id) => { if (confirm('ลบข่าว?')) { await newsService.deleteNews(id); fetchNews() } }
const createNews = () => router.push('/organizer/create-news')
const switchToManageTab = () => (activeTab.value = 'home')

// ⭐ onMounted - เรียกใช้ฟังก์ชันทั้งหมด
onMounted(async () => {
  const status = localStorage.getItem('organizer_status')
  
  if (status !== 'approved') {
      try {
          const res = await apiClient.get('/auth/me/')
          if (res.data.organizer_status !== 'approved') {
              throw new Error('Not approved')
          }
          localStorage.setItem('organizer_status', 'approved')
          userProfile.value = res.data
          console.log('✅ [OrganizerDashboard] Profile loaded:', res.data.username)
      } catch (e) {
          alert('คุณไม่มีสิทธิ์เข้าถึงหน้านี้ กรุณาสมัครเป็นผู้จัดกิจกรรมก่อน')
          router.push('/')
          return
      }
  } else {
      try {
          const res = await apiClient.get('/auth/me/')
          userProfile.value = res.data
          console.log('✅ [OrganizerDashboard] Profile loaded:', res.data.username)
      } catch (e) {
          console.error('Failed to load profile:', e)
      }
  }

  document.addEventListener('click', handleClickOutside)
  fetchActivities()
  fetchNews()
  fetchFacultyStatistics()      // ⭐ ดึงสัดส่วนคณะ
  fetchRegistrationTrend()       // ⭐ ดึงแนวโน้มการลงทะเบียน
})

onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>