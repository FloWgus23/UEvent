<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F] flex flex-col relative overflow-hidden">
    
    <div class="absolute top-0 left-0 w-full h-[400px] bg-gradient-to-b from-[#1E3A8A]/10 via-blue-100/20 to-transparent pointer-events-none"></div>
    <div class="absolute -top-[20%] -right-[10%] w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[100px] pointer-events-none"></div>
    <div class="absolute top-[20%] -left-[10%] w-[500px] h-[500px] bg-purple-400/10 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="container mx-auto px-6 py-8 relative z-10">
      
      <button 
        @click="goBack" 
        class="group flex items-center gap-2 text-gray-500 hover:text-[#1E3A8A] transition-colors mb-6 md:mb-0 md:absolute md:top-8 md:left-6 font-medium"
      >
        <div class="w-10 h-10 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center group-hover:border-blue-200 group-hover:bg-blue-50 transition-all">
          <i class="fa-solid fa-arrow-left text-sm group-hover:-translate-x-1 transition-transform"></i>
        </div>
        <span>กลับหน้าหลัก</span>
      </button>

      <div class="flex flex-col items-center justify-center min-h-[85vh]">
        
        <div class="w-full max-w-4xl bg-white/95 rounded-[32px] shadow-[0_20px_60px_-15px_rgba(30,58,138,0.12)] overflow-hidden animate-fade-in-up border border-white relative backdrop-blur-xl">
          
          <div class="p-8 md:p-14">
            
            <div class="text-center mb-10">
              <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-[#1E3A8A] to-[#3B82F6] text-white shadow-lg shadow-blue-500/30 mb-6 transform hover:scale-105 transition-transform">
                <i class="fa-solid fa-id-card-clip text-3xl"></i>
              </div>
              <h1 class="text-3xl md:text-4xl font-bold tracking-tight mb-3 text-gray-900">
                ยืนยันตัวตนผู้จัดกิจกรรม
              </h1>
              <p class="text-gray-500 max-w-lg mx-auto leading-relaxed mb-6">
                เพื่อสร้างความน่าเชื่อถือให้กับ Community ของ UEvent <br class="hidden md:block">
                กรุณาเตรียมเอกสารเพื่อยืนยันตัวตนของคุณ
              </p>
              
              <div class="inline-flex items-center gap-3 bg-amber-50 border border-amber-200 px-6 py-3 rounded-xl text-amber-800 font-medium text-sm shadow-sm animate-fade-in">
                <div class="bg-amber-100 text-amber-600 w-8 h-8 rounded-full flex items-center justify-center shrink-0">
                  <i class="fa-solid fa-circle-exclamation"></i>
                </div>
                <span>เลือกแนบเอกสาร <span class="font-bold text-amber-900 underline decoration-2 underline-offset-2">เพียง 1 อย่าง</span> จากรายการด้านล่าง</span>
              </div>
            </div>
                
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 mb-12">
              
              <div class="animate-fade-in-up bg-gradient-to-br from-white to-blue-50/50 p-6 rounded-2xl text-center border border-blue-100 hover:border-blue-300 hover:shadow-[0_8px_30px_rgb(59,130,246,0.12)] hover:-translate-y-1 transition-all duration-300 group" style="animation-delay: 0.2s; animation-fill-mode: both;">
                <div class="w-14 h-14 mx-auto bg-blue-100/50 rounded-full flex items-center justify-center mb-4 group-hover:bg-blue-500 transition-colors duration-300">
                  <i class="fa-regular fa-id-card text-2xl text-blue-500 group-hover:text-white transition-colors"></i>
                </div>
                <h3 class="font-bold text-gray-800 text-sm">บัตรประชาชน</h3>
                <p class="text-xs text-gray-500 mt-1">เห็นชื่อ-นามสกุลชัดเจน</p>
              </div>

              <div class="animate-fade-in-up bg-gradient-to-br from-white to-purple-50/50 p-6 rounded-2xl text-center border border-purple-100 hover:border-purple-300 hover:shadow-[0_8px_30px_rgb(168,85,247,0.12)] hover:-translate-y-1 transition-all duration-300 group" style="animation-delay: 0.3s; animation-fill-mode: both;">
                <div class="w-14 h-14 mx-auto bg-purple-100/50 rounded-full flex items-center justify-center mb-4 group-hover:bg-purple-500 transition-colors duration-300">
                  <i class="fa-solid fa-graduation-cap text-2xl text-purple-500 group-hover:text-white transition-colors"></i>
                </div>
                <h3 class="font-bold text-gray-800 text-sm">บัตรนักศึกษา</h3>
                <p class="text-xs text-gray-500 mt-1">สำหรับกิจกรรมในมหาวิทยาลัย</p>
              </div>

              <div class="animate-fade-in-up bg-gradient-to-br from-white to-teal-50/50 p-6 rounded-2xl text-center border border-teal-100 hover:border-teal-300 hover:shadow-[0_8px_30px_rgb(20,184,166,0.12)] hover:-translate-y-1 transition-all duration-300 group" style="animation-delay: 0.4s; animation-fill-mode: both;">
                <div class="w-14 h-14 mx-auto bg-teal-100/50 rounded-full flex items-center justify-center mb-4 group-hover:bg-teal-500 transition-colors duration-300">
                  <i class="fa-solid fa-building-columns text-2xl text-teal-500 group-hover:text-white transition-colors"></i>
                </div>
                <h3 class="font-bold text-gray-800 text-sm">หนังสือรับรอง</h3>
                <p class="text-xs text-gray-500 mt-1">จากหน่วยงานหรือคณะ</p>
              </div>

            </div>

            <form @submit.prevent="handleSubmit">
              <div class="space-y-8">
                
                <div 
                  class="relative w-full border-[3px] border-dashed rounded-[24px] transition-all duration-300 cursor-pointer group overflow-hidden bg-gray-50/30"
                  :class="[
                    isDragging 
                      ? 'border-[#3B82F6] bg-blue-50/80 scale-[1.02] shadow-inner' 
                      : 'border-gray-200 hover:border-[#3B82F6] hover:bg-blue-50/30',
                    selectedFile ? 'border-solid border-green-400 bg-green-50/30' : ''
                  ]"
                  @click="$refs.fileInput.click()"
                  @dragover.prevent="isDragging = true"
                  @dragleave.prevent="isDragging = false"
                  @drop.prevent="handleDrop"
                >
                  <input 
                    type="file" 
                    ref="fileInput" 
                    class="hidden" 
                    accept="image/jpeg,image/png,application/pdf" 
                    @change="handleFileSelect"
                  >

                  <div class="px-6 py-12 flex flex-col items-center justify-center text-center relative z-10">
                    
                    <div v-if="!selectedFile" class="transition-transform duration-300 group-hover:-translate-y-2 animate-fade-in-up" style="animation-delay: 0.5s; animation-fill-mode: both;">
                      <div class="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-5 shadow-sm border border-blue-100 group-hover:bg-blue-100 group-hover:shadow-md transition-all">
                        <i class="fa-solid fa-cloud-arrow-up text-3xl text-blue-500 group-hover:text-blue-600 transition-colors"></i>
                      </div>
                      <h3 class="text-lg font-bold text-gray-800 mb-2">อัปโหลดไฟล์เอกสาร (เลือก 1 อย่าง)</h3>
                      <p class="text-sm text-gray-500">รองรับ JPG, PNG หรือ PDF (สูงสุด 5MB)</p>
                    </div>

                    <div v-else class="w-full flex flex-col items-center animate-fade-in">
                      <div class="mb-5 relative animate-pop-in">
                        <div class="absolute -inset-4 bg-gradient-to-br from-green-100 to-transparent rounded-full opacity-50 blur-lg"></div>
                        <i v-if="selectedFile.type.includes('pdf')" class="fa-solid fa-file-pdf text-6xl text-red-500 drop-shadow-md relative z-10"></i>
                        <i v-else class="fa-solid fa-file-image text-6xl text-green-500 drop-shadow-md relative z-10"></i>
                      </div>
                      
                      <div class="bg-white px-6 py-3 rounded-2xl flex items-center gap-4 max-w-md border border-green-200 shadow-sm animate-pop-in" style="animation-delay: 0.1s; animation-fill-mode: both;">
                        <div class="text-left overflow-hidden">
                          <p class="text-sm font-bold text-gray-800 truncate">{{ selectedFile.name }}</p>
                          <p class="text-xs text-gray-500">{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB</p>
                        </div>
                        <button @click.stop="clearFile" type="button" class="w-8 h-8 rounded-full bg-gray-100 hover:bg-red-500 hover:text-white text-gray-500 transition-colors flex items-center justify-center flex-shrink-0">
                          <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                      </div>
                      <p class="mt-4 text-green-600 text-sm font-bold flex items-center gap-2 bg-green-50 border border-green-100 px-4 py-1.5 rounded-full animate-pop-in" style="animation-delay: 0.2s; animation-fill-mode: both;">
                        <i class="fa-solid fa-circle-check"></i> พร้อมอัปโหลด
                      </p>
                    </div>
                  </div>
                </div>

                <div class="flex justify-center pt-2 animate-fade-in-up" style="animation-delay: 0.6s; animation-fill-mode: both;">
                  <button 
                    type="submit" 
                    :disabled="!selectedFile || isSubmitting"
                    class="w-full md:w-auto min-w-[240px] px-8 py-4 bg-gradient-to-r from-[#1E3A8A] via-[#2563EB] to-[#3B82F6] hover:from-[#1e3a8a] hover:via-[#1d4ed8] hover:to-[#2563eb] text-white rounded-xl font-bold shadow-[0_10px_20px_-10px_rgba(37,99,235,0.5)] transition-all transform hover:-translate-y-1 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none flex items-center justify-center gap-3 text-base"
                  >
                    <i v-if="isSubmitting" class="fa-solid fa-spinner fa-spin"></i>
                    <span>{{ isSubmitting ? 'กำลังส่งข้อมูล...' : 'ยืนยันการสมัคร' }}</span>
                  </button>
                </div>

              </div>
            </form>

          </div>
        </div>
        
        <p class="mt-8 text-xs text-gray-400 flex items-center gap-1.5 opacity-80">
          <i class="fa-solid fa-shield-halved"></i> ข้อมูลของคุณจะถูกเก็บเป็นความลับตามนโยบายความเป็นส่วนตัว
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'

const router = useRouter()
const fileInput = ref(null)
const selectedFile = ref(null)
const isSubmitting = ref(false)
const isDragging = ref(false)

const goBack = () => {
  router.push('/')
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  validateAndSetFile(file)
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  validateAndSetFile(file)
}

const validateAndSetFile = (file) => {
  if (!file) return
  
  const validTypes = ['image/jpeg', 'image/png', 'application/pdf']
  if (!validTypes.includes(file.type)) {
    alert('รูปแบบไฟล์ไม่ถูกต้อง กรุณาใช้ไฟล์ JPG, PNG หรือ PDF')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    alert('ขนาดไฟล์ต้องไม่เกิน 5MB')
    return
  }

  selectedFile.value = file
}

const clearFile = () => {
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}

const handleSubmit = async () => {
  if (!selectedFile.value) return

  try {
    isSubmitting.value = true
    
    const formData = new FormData()
    formData.append('document', selectedFile.value)

    await authService.requestOrganizer(formData)    

    localStorage.setItem('organizer_status', 'pending')
    
    router.push('/waiting-approval').then(() => {
        window.location.reload()
    })

  } catch (error) {
    console.error(error)
    const msg = error.response?.data?.message || 'เกิดข้อผิดพลาดในการส่งข้อมูล'
    alert(`เกิดข้อผิดพลาด: ${msg}`)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

/* Animations */
.animate-fade-in-up {
  animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

/* เพิ่มคลาสสำหรับเอฟเฟกต์เด้งป๊อปอัป */
.animate-pop-in {
  animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  opacity: 0;
  transform: scale(0.8);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Keyframes สำหรับเอฟเฟกต์ป๊อปอัป */
@keyframes popIn {
  0% { transform: scale(0.8); opacity: 0; }
  50% { transform: scale(1.15); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
</style>