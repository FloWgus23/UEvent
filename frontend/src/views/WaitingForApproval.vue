<template>
  <div class="min-h-screen bg-[#F8FAFC] font-sans flex items-center justify-center p-6 relative overflow-hidden">
    
    <div class="absolute top-0 left-0 w-full h-[600px] bg-gradient-to-b from-[#EFF6FF] to-transparent pointer-events-none"></div>
    <div class="absolute -top-[10%] -right-[5%] w-[500px] h-[500px] bg-blue-100/50 rounded-full blur-[80px]"></div>
    <div class="absolute bottom-0 left-0 w-[400px] h-[400px] bg-indigo-50/50 rounded-full blur-[100px]"></div>

    <div class="w-full max-w-2xl bg-white rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.08)] border border-white/80 relative z-10 animate-fade-in-up overflow-hidden">
      
      <div class="bg-gradient-to-r from-[#1E3A8A] to-[#2563EB] h-2"></div>

      <div class="p-8 md:p-14 text-center">
        
        <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-blue-50 text-[#1E3A8A] mb-8 relative">
          <div class="absolute inset-0 rounded-full border-4 border-blue-50 animate-ping opacity-20"></div>
          <div class="absolute inset-0 rounded-full border border-blue-100"></div>
          <i class="fa-solid fa-hourglass-half text-4xl animate-pulse"></i>
        </div>

        <h1 class="text-3xl font-bold text-gray-900 mb-3 tracking-tight">อยู่ระหว่างการตรวจสอบ</h1>
        <p class="text-gray-500 text-sm mb-10 bg-gray-50 inline-block px-4 py-1.5 rounded-full border border-gray-100 font-mono">
          Ref ID: #REQ-{{ Math.floor(Math.random() * 1000000) }}
        </p>

        <div class="max-w-md mx-auto mb-12">
          <div class="relative flex justify-between items-center z-10">
            <div class="absolute top-1/2 left-0 w-full h-1 bg-gray-100 -z-10 -translate-y-1/2 rounded-full"></div>
            <div class="absolute top-1/2 left-0 w-1/2 h-1 bg-gradient-to-r from-blue-400 to-blue-600 -z-10 -translate-y-1/2 rounded-full shadow-sm"></div>

            <div class="flex flex-col items-center gap-2">
              <div class="w-9 h-9 rounded-full bg-green-500 text-white flex items-center justify-center shadow-lg ring-4 ring-white transition-transform hover:scale-110">
                <i class="fa-solid fa-check text-xs"></i>
              </div>
              <span class="text-xs font-bold text-gray-600 uppercase tracking-wide">ส่งเอกสาร</span>
            </div>

            <div class="flex flex-col items-center gap-2">
              <div class="w-10 h-10 rounded-full bg-[#1E3A8A] text-white flex items-center justify-center shadow-xl shadow-blue-200 ring-4 ring-white relative z-10 scale-110">
                <i class="fa-solid fa-magnifying-glass text-sm animate-tada"></i>
                <div class="absolute -top-1.5 -right-1.5 w-3.5 h-3.5 bg-yellow-400 rounded-full border-2 border-white animate-bounce"></div>
              </div>
              <span class="text-xs font-bold text-[#1E3A8A] uppercase tracking-wide">กำลังตรวจสอบ</span>
            </div>

            <div class="flex flex-col items-center gap-2 opacity-40">
              <div class="w-9 h-9 rounded-full bg-gray-200 text-gray-500 flex items-center justify-center ring-4 ring-white">
                <i class="fa-solid fa-gavel text-xs"></i>
              </div>
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wide">อนุมัติ</span>
            </div>
          </div>
        </div>

        <div class="bg-[#F8FAFC] rounded-2xl p-6 border border-gray-100 mb-10 text-left relative overflow-hidden group">
          <div class="absolute top-0 right-0 w-20 h-20 bg-blue-100/50 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none transition-opacity group-hover:opacity-75"></div>
          
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center text-blue-600 shadow-sm border border-gray-100 flex-shrink-0">
               <i class="fa-solid fa-circle-info text-lg"></i>
            </div>
            <div>
              <h3 class="font-bold text-gray-900 mb-1">ขั้นตอนต่อไป</h3>
              <p class="text-sm text-gray-600 leading-relaxed">
                เจ้าหน้าที่จะตรวจสอบความถูกต้องของเอกสาร โดยอาจใช้เวลา <strong>อย่างน้อย 24 ชั่วโมง (หรือมากกว่านั้น)</strong> <br>
                เมื่ออนุมัติแล้ว คุณจะได้รับสิทธิ์ <strong>"ผู้จัดกิจกรรม"</strong> และเริ่มสร้างกิจกรรมได้ทันที
              </p>
            </div>
          </div>
        </div>

        <div class="flex justify-center">
          <button 
            @click="$router.push('/')" 
            class="px-10 py-4 rounded-xl bg-gradient-to-r from-[#1E3A8A] to-[#2563EB] hover:to-[#1D4ED8] text-white font-bold shadow-lg shadow-blue-900/20 transition-all transform hover:-translate-y-1 active:translate-y-0 text-base min-w-[200px]"
          >
            กลับสู่หน้าหลัก
          </button>
        </div>

      </div>
      
      <div class="bg-gray-50/80 px-8 py-4 border-t border-gray-100 text-center backdrop-blur-sm">
         <p class="text-[10px] text-gray-400 flex items-center justify-center gap-1.5">
           <i class="fa-solid fa-shield-halved"></i> ข้อมูลของคุณได้รับการปกป้องด้วยมาตรฐานความปลอดภัยระดับสูง
         </p>
      </div>

    </div>
  </div>
</template>

<script setup>
// Static Page displaying status
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes tada {
  0% { transform: scale(1); }
  10%, 20% { transform: scale(0.9) rotate(-3deg); }
  30%, 50%, 70%, 90% { transform: scale(1.1) rotate(3deg); }
  40%, 60%, 80% { transform: scale(1.1) rotate(-3deg); }
  100% { transform: scale(1) rotate(0); }
}

.animate-tada {
  animation: tada 2s infinite;
}
</style>