<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F]">
    
    <Navbar />

    <div class="pt-28 pb-8 px-6 bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">กิจกรรมของฉัน</h1>
            <p class="text-gray-500 mt-2">ประวัติการลงทะเบียนทั้งหมดของคุณ</p>
          </div>
          
          <div class="flex items-center gap-3 bg-blue-50 px-4 py-2 rounded-xl border border-blue-100">
            <div class="text-right">
              <div class="text-2xl font-bold text-blue-600 leading-none">{{ registrations.length }}</div>
              <div class="text-xs text-blue-400 font-medium uppercase tracking-wide">รายการ</div>
            </div>
            <i class="fa-solid fa-ticket text-blue-200 text-3xl"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <div class="flex flex-wrap gap-2 mb-8">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="currentTab = tab.value"
          :class="[
            'px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-200 border',
            currentTab === tab.value
              ? 'bg-[#1E3A8A] text-white border-[#1E3A8A] shadow-md transform scale-105'
              : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300 hover:bg-gray-50'
          ]"
        >
          {{ tab.label }} 
          <span class="ml-1.5 px-1.5 py-0.5 rounded-md text-xs font-bold" :class="currentTab === tab.value ? 'bg-white/20 text-white' : 'bg-gray-100 text-gray-500'">
            {{ getTabCount(tab.value) }}
          </span>
        </button>
      </div>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
        <div class="w-12 h-12 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin"></div>
        <p class="mt-4 text-gray-400 font-medium animate-pulse">กำลังโหลดข้อมูล...</p>
      </div>

      <div v-else-if="filteredActivities.length === 0" class="text-center py-24 bg-white rounded-[32px] border border-dashed border-gray-200 shadow-sm">
        <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-300">
          <i class="fa-regular fa-calendar-xmark text-4xl"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">ไม่มีรายการในหมวดนี้</h3>
        <p class="text-gray-500 mb-6">คุณยังไม่มีกิจกรรมในสถานะนี้</p>
        <router-link to="/" class="inline-flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 transition shadow-lg shadow-blue-200">
          <i class="fa-solid fa-search"></i> ค้นหากิจกรรม
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 gap-6">
        <div
          v-for="registration in filteredActivities"
          :key="registration.id"
          class="group bg-white rounded-[24px] shadow-[0_2px_12px_rgba(0,0,0,0.04)] hover:shadow-[0_12px_30px_rgba(0,0,0,0.08)] hover:-translate-y-1 transition-all duration-300 overflow-hidden border border-gray-100 flex flex-col md:flex-row"
        >
          <div class="md:w-80 h-56 md:h-auto relative overflow-hidden bg-gray-100 shrink-0">
            <img
              :src="registration.activity.image || 'https://via.placeholder.com/800x600'"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
              alt="Activity"
            />
            <div class="absolute top-4 left-4">
               <span :class="['px-3 py-1.5 rounded-lg text-xs font-bold shadow-sm backdrop-blur-md border border-white/20 uppercase tracking-wide', getStatusColor(registration.activity.status)]">
                  {{ registration.activity.status }}
               </span>
            </div>
          </div>

          <div class="flex-1 p-6 md:p-8 flex flex-col">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1">
                {{ registration.activity.name }}
              </h3>
            </div>

            <p class="text-gray-500 text-sm mb-6 line-clamp-2 leading-relaxed">
              {{ registration.activity.description }}
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-y-3 gap-x-6 mb-6 text-sm">
              <div class="flex items-center text-gray-600 bg-gray-50 px-3 py-2 rounded-lg">
                <i class="fa-regular fa-calendar w-5 text-center text-blue-500 mr-2"></i>
                <span>{{ formatDate(registration.activity.date) }}</span>
              </div>
              <div class="flex items-center text-gray-600 bg-gray-50 px-3 py-2 rounded-lg">
                <i class="fa-regular fa-clock w-5 text-center text-blue-500 mr-2"></i>
                <span>{{ registration.activity.time_display || 'ไม่ระบุเวลา' }}</span>
              </div>
              <div class="flex items-center text-gray-600 bg-gray-50 px-3 py-2 rounded-lg col-span-1 sm:col-span-2">
                <i class="fa-solid fa-location-dot w-5 text-center text-blue-500 mr-2"></i>
                <span class="truncate">{{ registration.activity.location }}</span>
              </div>
            </div>

            <div class="mt-auto pt-6 border-t border-gray-100 flex flex-wrap gap-3 items-center justify-between">
              <div class="text-xs text-gray-400">
                ลงทะเบียนเมื่อ: {{ formatDateTime(registration.registered_at) }}
              </div>
              
              <div class="flex gap-3 w-full sm:w-auto">
                <button
                  v-if="registration.status === 'registered'"
                  @click="confirmCancel(registration.id)"
                  class="flex-1 sm:flex-none px-5 py-2.5 bg-white border border-red-200 text-red-600 rounded-xl hover:bg-red-50 hover:border-red-300 transition text-sm font-medium"
                >
                  ยกเลิก
                </button>
                <router-link
                  :to="`/activity/${registration.activity.id}`"
                  class="flex-1 sm:flex-none px-6 py-2.5 bg-[#1E3A8A] text-white rounded-xl hover:bg-[#1E40AF] transition text-sm font-medium shadow-md hover:shadow-lg flex items-center justify-center gap-2"
                >
                  รายละเอียด <i class="fa-solid fa-arrow-right text-xs"></i>
                </router-link>
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
import apiClient from '@/services/api.js'

const router = useRouter()

const registrations = ref([])
const isLoading = ref(false)
const showDropdown = ref(false)
const currentTab = ref('all')

const tabs = [
  { label: 'ทั้งหมด', value: 'all' },
  { label: 'กำลังรับสมัคร', value: 'กำลังรับสมัคร' },
  { label: 'กำลังดำเนินการ', value: 'กำลังดำเนินการ' },
  { label: 'สิ้นสุดแล้ว', value: 'สิ้นสุดแล้ว' }
]

// Computed
const filteredActivities = computed(() => {
  if (currentTab.value === 'all') {
    return registrations.value
  }
  return registrations.value.filter(r => r.activity.status === currentTab.value)
})

const getTabCount = (tab) => {
  if (tab === 'all') return registrations.value.length
  return registrations.value.filter(r => r.activity.status === tab).length
}

// Functions
const fetchMyActivities = async () => {
  try {
    isLoading.value = true
    const response = await apiClient.get('/my-registrations/')
    registrations.value = response.data
  } catch (error) {
    console.error('Error fetching registrations:', error)
    if (error.response?.status === 401) {
      router.push('/login')
    }
  } finally {
    isLoading.value = false
  }
}

const confirmCancel = async (registrationId) => {
  if (!confirm('คุณต้องการยกเลิกการลงทะเบียนหรือไม่?')) return

  try {
    await apiClient.delete(`/registrations/${registrationId}/cancel/`)
    alert('✅ ยกเลิกการลงทะเบียนสำเร็จ')
    fetchMyActivities()
  } catch (error) {
    console.error('Error canceling registration:', error)
    alert('❌ ไม่สามารถยกเลิกได้')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })
}

const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('th-TH', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const getStatusColor = (status) => {
  const colors = {
    'กำลังรับสมัคร': 'bg-green-500/10 text-green-700 border-green-200',
    'กำลังดำเนินการ': 'bg-blue-500/10 text-blue-700 border-blue-200',
    'สิ้นสุดแล้ว': 'bg-gray-500/10 text-gray-700 border-gray-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-700'
}

const toggleDropdown = () => showDropdown.value = !showDropdown.value
const closeDropdown = () => showDropdown.value = false
const handleClickOutside = (e) => { if (!e.target.closest('.relative')) closeDropdown() }
const handleLogout = () => { localStorage.clear(); router.push('/login') }

onMounted(() => {
  fetchMyActivities()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
</style>

<style scoped>
.font-sans { font-family: 'Inter', sans-serif; }
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

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