<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900">
    <!-- Header -->
    <header class="bg-blue-900/50 backdrop-blur-sm shadow-lg">
      <div class="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
        <h1 class="text-white text-3xl font-bold">UEvent</h1>
        <button
          @click="goBack"
          class="text-white text-lg hover:text-blue-200 transition-colors flex items-center gap-2"
        >
          <i class="fa-solid fa-arrow-left"></i>
          กลับ
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-8 py-12">
      <div class="bg-white rounded-3xl shadow-2xl p-10">
        <!-- Activity Info Header -->
        <div class="mb-8 pb-6 border-b-2 border-gray-200">
          <h2 class="text-3xl font-bold text-gray-800 mb-2">{{ activityName }}</h2>
          <p class="text-gray-600">
            <i class="fa-solid fa-calendar mr-2"></i>{{ activityDate }}
            <span class="mx-4">|</span>
            <i class="fa-solid fa-location-dot mr-2"></i>{{ activityLocation }}
          </p>
          <div class="mt-4 flex items-center gap-4">
            <span class="text-2xl font-bold text-blue-600">
              {{ registrations.length }} / {{ activityCapacity }} คน
            </span>
            <span
              :class="[
                'px-4 py-2 rounded-lg font-semibold text-sm',
                activityStatus === 'กำลังรับสมัคร'
                  ? 'bg-blue-100 text-blue-700'
                  : activityStatus === 'กำลังดำเนินการ'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-red-100 text-red-700'
              ]"
            >
              {{ activityStatus }}
            </span>
          </div>
        </div>

        <!-- Search and Filter -->
        <div class="mb-6 flex gap-4">
          <div class="flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="ค้นหาชื่อผู้ลงทะเบียน..."
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
            />
          </div>
          <button
            @click="exportToCSV"
            class="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-semibold flex items-center gap-2"
          >
            <i class="fa-solid fa-file-excel"></i>
            ส่งออก Excel
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-12 text-gray-500 text-lg">
          กำลังโหลดข้อมูล...
        </div>

        <!-- Empty State -->
        <div v-else-if="registrations.length === 0" class="text-center py-12">
          <i class="fa-solid fa-users text-6xl text-gray-300 mb-4"></i>
          <p class="text-gray-500 text-lg">ยังไม่มีผู้ลงทะเบียนในกิจกรรมนี้</p>
        </div>

        <!-- Registrations Table -->
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="text-left border-b-2 border-gray-200">
                <th class="pb-4 text-gray-700 font-semibold text-lg">#</th>
                <th class="pb-4 text-gray-700 font-semibold text-lg">ชื่อผู้ใช้</th>
                <th class="pb-4 text-gray-700 font-semibold text-lg">อีเมล</th>
                <th class="pb-4 text-gray-700 font-semibold text-lg">เบอร์โทร</th>
                <th class="pb-4 text-gray-700 font-semibold text-lg">หมายเหตุ</th>
                <th class="pb-4 text-gray-700 font-semibold text-lg">วันที่ลงทะเบียน</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="(registration, index) in filteredRegistrations"
                :key="registration.id"
                class="border-b border-gray-100 hover:bg-gray-50 transition"
              >
                <td class="py-6">{{ index + 1 }}</td>
                <td class="py-6 font-semibold">{{ registration.user_name }}</td>
                <td class="py-6">{{ registration.user_email }}</td>
                <td class="py-6">{{ registration.phone || '-' }}</td>
                <td class="py-6">{{ registration.note || '-' }}</td>
                <td class="py-6">{{ formatDate(registration.registered_at) }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div class="flex justify-center items-center gap-4 mt-6">
            <button
              class="px-5 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg"
              :disabled="currentPage === 1"
              @click="prevPage"
            >
              ก่อนหน้า
            </button>

            <span class="text-gray-700 font-semibold">
              หน้า {{ currentPage }} / {{ totalPages }}
            </span>

            <button
              class="px-5 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg"
              :disabled="currentPage === totalPages"
              @click="nextPage"
            >
              ถัดไป
            </button>
          </div>
        </div>
      </div>
    </div>

    <footer class="bg-blue-900/50 backdrop-blur-sm text-white py-6 mt-12 text-center">
      <h3 class="text-xl font-bold">UEvent</h3>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import activityService from '@/services/activityService.js'

const router = useRouter()
const route = useRoute()

const activityId = route.params.id
const activityName = ref('')
const activityDate = ref('')
const activityLocation = ref('')
const activityCapacity = ref(0)
const activityStatus = ref('')

const registrations = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

const goBack = () => {
  router.push('/organizer/dashboard')
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  if (Number.isNaN(date.getTime())) return '-'
  
  const months = [
    'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
    'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
  ]
  
  return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear() + 543} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')} น.`
}

const formatDateOnly = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  if (Number.isNaN(date.getTime())) return '-'
  
  const months = [
    'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
    'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
  ]
  
  return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear() + 543}`
}

const fetchActivityAndRegistrations = async () => {
  try {
    isLoading.value = true

    // ดึงข้อมูลกิจกรรม
    const activityResponse = await activityService.getActivityById(activityId)
    activityName.value = activityResponse.data.name
    activityDate.value = formatDateOnly(activityResponse.data.date)
    activityLocation.value = activityResponse.data.location
    activityCapacity.value = activityResponse.data.capacity
    activityStatus.value = activityResponse.data.status

    // ดึงรายชื่อผู้ลงทะเบียน
    const registrationsResponse = await activityService.getActivityRegistrations(activityId)
    registrations.value = registrationsResponse.data
  } catch (error) {
    console.error('Error fetching data:', error)
    alert('เกิดข้อผิดพลาดในการโหลดข้อมูล')
  } finally {
    isLoading.value = false
  }
}

const filteredRegistrations = computed(() => {
  let filtered = registrations.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(
      (r) =>
        r.user_name?.toLowerCase().includes(query) ||
        r.user_email?.toLowerCase().includes(query) ||
        r.phone?.toLowerCase().includes(query)
    )
  }

  const start = (currentPage.value - 1) * itemsPerPage
  return filtered.slice(start, start + itemsPerPage)
})

const totalPages = computed(() =>
  Math.ceil(registrations.value.length / itemsPerPage) || 1
)

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const exportToCSV = () => {
  if (registrations.value.length === 0) {
    alert('ไม่มีข้อมูลให้ส่งออก')
    return
  }

  const headers = ['ลำดับ', 'ชื่อผู้ใช้', 'อีเมล', 'เบอร์โทร', 'หมายเหตุ', 'วันที่ลงทะเบียน']
  const rows = registrations.value.map((r, index) => [
  index + 1,
  r.user_name || '-',
  r.user_email || '-',
  r.phone ? `="${r.phone}"` : '-',   // 👈 แก้ตรงนี้ ป้องกัน Scientific Notation
  r.note || '-',
  formatDate(r.registered_at)
  ])

  const activityInfo = [
  `"ชื่อกิจกรรม","${activityName.value}"`,
  `"วันที่จัด",="${activityDate.value}"`,    // 👈 เปลี่ยนจาก "'${...}" เป็น ="${...}"
  `"สถานที่","${activityLocation.value}"`,
  `"จำนวนผู้ลงทะเบียน","${registrations.value.length}/${activityCapacity.value} คน"`,
  ``
  ]

  const csvContent = [
  '\ufeff' + activityInfo.join('\n'),
  headers.join(','),
  ...rows.map((row) =>
    row.map((cell) =>
      // ถ้า cell เริ่มต้นด้วย =" แสดงว่า format แล้ว ไม่ต้อง wrap เพิ่ม
      String(cell).startsWith('="') ? cell : `"${cell}"`
    ).join(',')
  )
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `registrations_${activityName.value}_${Date.now()}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  fetchActivityAndRegistrations()
})
</script>