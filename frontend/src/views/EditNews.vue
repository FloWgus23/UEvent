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

          <div class="relative">
            <button 
              @click="toggleDropdown"
              class="w-12 h-12 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition"
            >
              <svg class="w-6 h-6 text-blue-900" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                  clip-rule="evenodd"
                />
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

    <!-- Main -->
    <div class="max-w-4xl mx-auto px-8 py-12">
      <div class="bg-white rounded-3xl shadow-2xl p-10">

        <h2 class="text-3xl font-bold text-gray-800 mb-8">แก้ไขข่าว</h2>

        <form @submit.prevent="handleSubmit" class="space-y-6">

          <!-- Title ชื่อข่าว -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">ชื่อข่าว</label>
            <input
              v-model="formData.title"
              type="text"
              class="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus-ring"
              required
            />
          </div>

          <!-- Content รายละเอียด-->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">รายละเอียดข่าว</label>
            <textarea
              v-model="formData.content"
              rows="4"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring resize-none"
              required
            ></textarea>
          </div>

          <!-- Date วันเวลา -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">วันที่</label>
            <input
              type="date"
              v-model="formData.date"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
            />
          </div>

          <!-- Location สถานที่ -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">สถานที่</label>
            <input
              v-model="formData.location"
              type="text"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
            />
          </div>

          <!-- Organization องค์กร -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">หน่วยงานองค์กร</label>
            <input
              v-model="formData.organization"
              type="text"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
            />
          </div>

          <!-- ⭐ Status  สถานะ-->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">สถานะข่าว</label>
            <select
              v-model="formData.status"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus-ring"
            >
              <option value="draft">ฉบับร่าง</option>
              <option value="published">เผยแพร่แล้ว</option>
            </select>
          </div>

          <!-- Image รูปภาพ -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">รูปปกข่าว</label>
            <div class="flex items-center gap-4">
              <input type="file" accept="image/*" id="image" @change="handleImageUpload" class="hidden" />
              <label for="image" class="px-6 py-3 bg-gray-100 border-2 border-gray-300 rounded-lg cursor-pointer hover:bg-gray-200 transition">
                เลือกไฟล์
              </label>
              <span class="text-gray-500 text-sm">{{ imageFileName || "ไม่ได้เลือกไฟล์ใด" }}</span>
            </div>

            <div v-if="imagePreview" class="mt-4">
              <img :src="imagePreview" class="w-64 rounded-lg shadow-lg" />
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex gap-4 pt-6">
            <button
              type="submit"
              class="flex-1 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition"
            >
              ✔ บันทึกการแก้ไข
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

    <footer class="bg-blue-900/50 backdrop-blur-sm text-white py-6 mt-12 text-center">
      <h3 class="text-xl font-bold">UEvent</h3>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import newsService from "@/services/newsService.js"

const router = useRouter()
const route = useRoute()

/* Dropdown */
const showDropdown = ref(false)
const toggleDropdown = () => showDropdown.value = !showDropdown.value
const closeDropdown = () => showDropdown.value = false

document.addEventListener("click", (e) => {
  if (!e.target.closest(".relative")) closeDropdown()
})

const handleLogout = () => {
  localStorage.removeItem("access")
  localStorage.removeItem("refresh")
  localStorage.removeItem("isAdmin")
  router.push("/")
}

/* Form */
const formData = ref({
  title: "",
  content: "",
  date: "",
  location: "",
  organization: "",
  status: "draft",   // ⭐ default
})

const imageFile = ref(null)
const imageFileName = ref("")
const imagePreview = ref("")

/* Load news */
const loadNews = async () => {
  try {
    const response = await newsService.getNews(route.params.id)
    const news = response.data

    formData.value.title = news.title
    formData.value.content = news.content
    formData.value.date = news.date
    formData.value.location = news.location
    formData.value.organization = news.organization
    formData.value.status = news.status     // ⭐ load status

    imagePreview.value = news.image
  } catch (err) {
    console.error(err)
    alert("โหลดข้อมูลข่าวล้มเหลว")
  }
}

onMounted(() => {
  loadNews()
})

/* Upload */
const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imageFileName.value = file.name
    imagePreview.value = URL.createObjectURL(file)
  }
}

/* Submit */
const handleSubmit = async () => {
  try {
    const data = new FormData()
    data.append("title", formData.value.title)
    data.append("content", formData.value.content)
    data.append("date", formData.value.date)
    data.append("location", formData.value.location)
    data.append("organization", formData.value.organization)
    data.append("status", formData.value.status)  // ⭐ send status

    if (imageFile.value) {
      data.append("image", imageFile.value)
    }

    await newsService.updateNews(route.params.id, data)

    alert("แก้ไขข่าวสำเร็จ!")
    router.push("/organizer/dashboard")

  } catch (err) {
    console.error(err)
    alert("เกิดข้อผิดพลาดในการแก้ไขข่าว")
  }
}
</script>

<style scoped>
.focus-ring {
  @apply focus:outline-none focus:ring-2 focus:ring-blue-400;
}
</style>
