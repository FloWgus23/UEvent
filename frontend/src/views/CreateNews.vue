<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900">
    
    <!-- Header -->
    <header class="bg-blue-900/50 backdrop-blur-sm shadow-lg border-b border-blue-700">
      <div class="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
        <h1 class="text-white text-3xl font-bold">UEvent</h1>

        <div class="flex items-center gap-8">
          <router-link
            to="/organizer/dashboard"
            class="text-white text-lg hover:text-blue-200 transition-colors"
          >
            หน้าแรก
          </router-link>

          <!-- Dropdown -->
          <div class="relative">
            <button 
              @click="toggleDropdown"
              class="w-12 h-12 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition"
            >
              <svg class="w-6 h-6 text-blue-900" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                      d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                      clip-rule="evenodd"/>
              </svg>
            </button>

            <div
              v-if="showDropdown"
              class="absolute right-0 mt-3 w-48 bg-white text-gray-800 rounded-lg shadow-xl py-2 z-50"
            >
              <router-link
                to="/profile"
                class="block px-4 py-3 hover:bg-blue-50"
                @click="closeDropdown"
              >
                <i class="fa-solid fa-user mr-2"></i> โปรไฟล์
              </router-link>

              <hr class="border-gray-300 my-1">

              <button
                class="w-full text-left px-4 py-3 text-red-500 hover:bg-red-50"
                @click="handleLogout"
              >
                <i class="fa-solid fa-right-from-bracket mr-2"></i> ออกจากระบบ
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="max-w-4xl mx-auto px-8 py-12">
      <div class="bg-white rounded-3xl shadow-2xl p-10">
        
        <h2 class="text-3xl font-bold text-gray-800 mb-8">สร้างข่าวสาร</h2>

        <form @submit.prevent="handleSubmit" class="space-y-6">

          <!-- ชื่อข่าว -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">ชื่อข่าว</label>
            <input
              v-model="formData.title"
              type="text"
              placeholder="เช่น ข่าวสารมออุบล"
              class="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus-ring"
              required
            />
          </div>

          <!-- รายละเอียดข่าว -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">รายละเอียดข่าว</label>
            <textarea
              v-model="formData.content"
              rows="4"
              placeholder="อธิบายเกี่ยวกับข่าว"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring resize-none"
              required
            ></textarea>
          </div>

          <!-- วันที่ลงข่าว -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">วันที่เวลา</label>
            <input
              type="date"
              v-model="formData.date"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
              required
            />
          </div>

          <!-- สถานที่ -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">สถานที่</label>
            <input
              v-model="formData.location"
              type="text"
              placeholder="เช่น มหาวิทยาลัยอุบลราชธานี"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
            />
          </div>

          <!-- หน่วยงาน -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">หน่วยงานองค์กร</label>
            <input
              v-model="formData.organization"
              type="text"
              placeholder="เช่น องค์การนักศึกษา"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
            />
          </div>

          <!-- สถานะข่าว -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">สถานะข่าว</label>

            <select
              v-model="formData.status"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
              required
            >
              <option disabled value="">-- เลือกสถานะ --</option>
              <option value="published">เผยแพร่แล้ว</option>
              <option value="draft">ฉบับร่าง</option>
            </select>
          </div>

          <!-- รูปภาพข่าว -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">รูปภาพข่าว</label>
            <div class="flex items-center gap-4">
              <input
                type="file"
                accept="image/*"
                id="image"
                @change="handleImageUpload"
                class="hidden"
              />
              <label
                for="image"
                class="px-6 py-3 bg-gray-100 border-2 border-gray-300 rounded-lg cursor-pointer hover:bg-gray-200 transition"
              >
                เลือกไฟล์
              </label>
              <span class="text-gray-500 text-sm">
                {{ imageFileName || "ไม่ได้เลือกไฟล์ใด" }}
              </span>
            </div>
          </div>

          <!-- ปุ่ม -->
          <div class="flex gap-4 pt-6">
            <button
              type="submit"
              class="flex-1 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition"
            >
              + สร้างข่าว
            </button>

            <button
              type="button"
              @click="router.push('/organizer/dashboard')"
              class="px-8 py-3 bg-white border-2 border-red-400 text-red-500 hover:bg-red-50 rounded-lg font-semibold"
            >
              ยกเลิก
            </button>
          </div>

        </form>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-blue-900/50 backdrop-blur-sm text-white py-6 mt-12 text-center">
      <h3 class="text-xl font-bold">UEvent</h3>
    </footer>

  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import newsService from "@/services/newsService.js"

const router = useRouter()

/* ========== DROPDOWN ========== */
const showDropdown = ref(false)

const toggleDropdown = () => (showDropdown.value = !showDropdown.value)
const closeDropdown = () => (showDropdown.value = false)

document.addEventListener("click", (e) => {
  if (!e.target.closest(".relative")) closeDropdown()
})

const handleLogout = () => {
  localStorage.removeItem("access")
  localStorage.removeItem("refresh")
  localStorage.removeItem("isAdmin")
  router.push("/")
}

/* ========== FORM DATA ========== */
const formData = ref({
  title: "",
  content: "",
  date: "",
  location: "",
  organization: "",
  status: "published"   // ⭐ default = เผยแพร่แล้ว
})

const imageFile = ref(null)
const imageFileName = ref("")

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imageFileName.value = file.name
  }
}

/* ========== SUBMIT ========== */
const handleSubmit = async () => {
  try {
    const data = new FormData()
    data.append("title", formData.value.title)
    data.append("content", formData.value.content)
    data.append("date", formData.value.date)
    data.append("location", formData.value.location)
    data.append("organization", formData.value.organization)
    data.append("status", formData.value.status) // ⭐ ส่งสถานะข่าวไป backend

    if (imageFile.value) {
      data.append("image", imageFile.value)
    }

    await newsService.createNews(data)

    alert("สร้างข่าวสำเร็จ!")
    router.push("/organizer/dashboard")

  } catch (err) {
    console.error(err)
    alert("เกิดข้อผิดพลาดในการสร้างข่าว")
  }
}
</script>

<style scoped>
.focus-ring {
  @apply focus:outline-none focus:ring-2 focus:ring-blue-400;
}
</style>
