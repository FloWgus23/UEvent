<template>
  <div class="min-h-screen bg-[#F5F7FA] font-sans text-[#1D1D1F]">

    <OnboardingModal />

    <div v-if="showToast" class="fixed top-24 left-1/2 -translate-x-1/2 z-50 pointer-events-none">
      <div :class="toastClass" class="px-6 py-3 rounded-full shadow-2xl text-white text-sm font-medium backdrop-blur-md bg-opacity-95 animate-fade-in-down pointer-events-auto flex items-center gap-2 border border-white/10">
        <i v-if="toastClass.includes('green')" class="fa-solid fa-check-circle"></i>
        <i v-else class="fa-solid fa-info-circle"></i>
        {{ toastMessage }}
      </div>
    </div>

    <nav class="fixed top-0 w-full z-40 bg-gradient-to-r from-[#0F172A] via-[#1E3A8A] to-[#1E40AF] text-white shadow-lg border-b border-white/10 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          
          <router-link to="/" class="text-2xl font-bold tracking-tight flex items-center gap-2 hover:opacity-90 transition-opacity">
            <i class="fa-solid fa-calendar-star text-white text-2xl drop-shadow-md"></i>
            <span class="font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-100">UEvent</span>
          </router-link>

          <div class="flex items-center gap-8">
            <div class="hidden md:flex items-center gap-6 text-[15px] font-medium text-blue-100">
              <router-link to="/" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all" active-class="text-white bg-white/10 font-bold shadow-sm">หน้าแรก</router-link>
              <router-link to="/category" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all" active-class="text-white bg-white/10 font-bold shadow-sm">หมวดหมู่</router-link>
              <router-link to="/news" class="hover:text-white hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all" active-class="text-white bg-white/10 font-bold shadow-sm">ข่าวสาร</router-link>
            </div>

            <div v-if="isLoggedIn" class="flex items-center gap-4">
              
              <div class="relative">
                <button @click.stop="toggleNotificationDropdown" class="text-blue-200 hover:text-white transition-colors relative p-2 rounded-full hover:bg-white/10">
                  <i class="fa-regular fa-bell text-xl"></i>
                  <span v-if="unreadCount > 0" class="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-[#1E3A8A] animate-pulse"></span>
                </button>

                <div v-if="showNotificationDropdown" class="absolute right-0 mt-3 w-80 bg-white/95 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-gray-100 py-2 z-50 transform origin-top-right transition-all animate-scale-in overflow-hidden flex flex-col" @click.stop>
                  <div class="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                    <h3 class="text-sm font-bold text-gray-800">การแจ้งเตือน</h3>
                    <button v-if="unreadCount > 0" @click="markAllAsRead" class="text-xs text-blue-600 hover:underline">อ่านทั้งหมด</button>
                  </div>
                  <div class="max-h-[350px] overflow-y-auto custom-scrollbar">
                    <div v-if="notifications.length === 0" class="p-8 text-center text-gray-400 text-sm">
                      <i class="fa-regular fa-bell-slash text-3xl mb-2 opacity-30 block"></i>
                      ไม่มีการแจ้งเตือนใหม่
                    </div>
                    <div 
                      v-for="item in notifications" 
                      :key="item.id"
                      class="px-4 py-3 hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-0 cursor-pointer flex gap-3 items-start relative group"
                      :class="{'bg-blue-50/30': !item.is_read}"
                      @click="handleReadNotification(item)"
                    >
                      <div class="mt-1 flex-shrink-0">
                         <i v-if="item.notification_type === 'success'" class="fa-solid fa-circle-check text-green-500 text-lg"></i>
                         <i v-else-if="item.notification_type === 'warning'" class="fa-solid fa-triangle-exclamation text-yellow-500 text-lg"></i>
                         <i v-else class="fa-solid fa-circle-info text-blue-500 text-lg"></i>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm text-gray-800 leading-tight mb-0.5" :class="{'font-bold': !item.is_read, 'font-medium': item.is_read}">{{ item.title }}</p>
                        <p class="text-xs text-gray-500 line-clamp-2 leading-snug">{{ item.message }}</p>
                        <p class="text-[10px] text-gray-400 mt-1.5">{{ formatDateAgo(item.created_at) }}</p>
                      </div>
                      <div v-if="!item.is_read" class="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0 animate-pulse"></div>
                      <button @click.stop="deleteNotification(item.id)" class="absolute right-2 top-2 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-1">
                        <i class="fa-solid fa-times text-xs"></i>
                      </button>
                    </div>
                  </div>
                  <router-link 
                    to="/notifications" 
                    class="block text-center py-3 text-xs font-semibold text-blue-600 bg-gray-50 hover:bg-blue-50 border-t border-gray-100 transition-colors"
                    @click="closeDropdown"
                  >
                    ดูการแจ้งเตือนทั้งหมด <i class="fa-solid fa-arrow-right ml-1"></i>
                  </router-link>
                </div>
              </div>

              <div class="relative">
                <button @click="toggleDropdown" class="flex items-center gap-2 hover:opacity-90 transition-opacity">
                  <div class="w-9 h-9 bg-white/10 rounded-full flex items-center justify-center border border-white/20 text-white overflow-hidden backdrop-blur-sm hover:bg-white/20 transition-all">
                    <img 
                      v-if="userProfile?.profile?.profile_image" 
                      :src="userProfile.profile.profile_image" 
                      alt="Profile"
                      class="w-full h-full object-cover"
                    />
                    <i v-else class="fa-solid fa-user text-sm"></i>
                  </div>
                </button>

                <div v-if="showDropdown" class="absolute right-0 mt-3 w-64 bg-white/95 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-gray-100 py-2 z-50 transform origin-top-right transition-all animate-scale-in" @click.stop>
                  <div class="px-5 py-3 border-b border-gray-100">
                    <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">บัญชีผู้ใช้</p>
                  </div>
                  <router-link to="/profile" class="dropdown-item" @click="closeDropdown">
                    <i class="fa-regular fa-id-card w-5 text-blue-600"></i> โปรไฟล์
                  </router-link>
                  <router-link to="/profile/activities" class="dropdown-item" @click="closeDropdown">
                    <i class="fa-regular fa-calendar-check w-5 text-green-600"></i> กิจกรรมของฉัน
                  </router-link>
                  <router-link to="/profile/dashboard" class="dropdown-item" @click="closeDropdown">
                    <i class="fa-solid fa-chart-line w-5 text-blue-600"></i> แดชบอร์ด
                  </router-link>
                  
                  <div v-if="organizerStatus === 'approved'">
                    <router-link to="/organizer/dashboard" class="dropdown-item font-semibold text-purple-700 bg-purple-50/50" @click="closeDropdown">
                        <i class="fa-solid fa-gauge-high w-5"></i> ผู้จัดกิจกรรม
                    </router-link>
                  </div>
                  <div v-else-if="organizerStatus === 'pending'">
                   <router-link to="/waiting-approval" class="dropdown-item text-yellow-600 bg-yellow-50 hover:bg-yellow-100" @click="closeDropdown">
                      <i class="fa-solid fa-clock w-5"></i> รออนุมัติ
                   </router-link>
                  </div>
                  <div v-else>
                    <button @click="requestOrganizer" class="dropdown-item text-blue-600 hover:bg-blue-50 w-full text-left">
                        <i class="fa-solid fa-briefcase w-5"></i> สมัครเป็นผู้จัด
                    </button>
                  </div>

                  <div class="border-t border-gray-100 my-1"></div>
                  <button @click="handleLogout" class="dropdown-item text-red-600 hover:bg-red-50">
                    <i class="fa-solid fa-arrow-right-from-bracket w-5"></i> ออกจากระบบ
                  </button>
                </div>
              </div>
            </div>

            <router-link v-else to="/login" class="bg-white text-blue-900 hover:bg-blue-50 px-5 py-2 rounded-full text-sm font-bold transition-all shadow-lg hover:shadow-xl transform active:scale-95">
              เข้าสู่ระบบ
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <div class="pt-32 pb-16 px-6 relative overflow-hidden bg-gradient-to-b from-[#0F172A] to-[#1E3A8A]">
      <div class="absolute top-0 left-1/4 w-[600px] h-[600px] bg-blue-500/20 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>
      <div class="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-indigo-500/20 rounded-full blur-[100px] pointer-events-none"></div>

      <div class="max-w-4xl mx-auto text-center mb-10 relative z-10">
        <h1 class="text-5xl md:text-6xl font-bold tracking-tight text-white mb-6 animate-fade-in-up drop-shadow-lg">
          ค้นหา <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-white">กิจกรรม</span> ที่ใช่
        </h1>
        <p class="text-xl text-blue-100 font-light max-w-2xl mx-auto animate-fade-in-up delay-100">
          เปิดประสบการณ์ใหม่ในรั้วมหาวิทยาลัย ค้นหาและเข้าร่วมกิจกรรมที่คุณสนใจได้ง่ายๆ
        </p>
      </div>

      <div class="max-w-3xl mx-auto relative z-10 animate-fade-in-up delay-200">
        <div class="relative group">
          <div class="absolute inset-0 bg-blue-400 rounded-full opacity-30 blur-xl group-hover:opacity-50 transition-opacity duration-500"></div>
          <div class="relative bg-white/10 backdrop-blur-md rounded-full shadow-2xl border border-white/20 flex items-center p-2 pl-6 transition-transform focus-within:scale-[1.01]">
            <i class="fa-solid fa-magnifying-glass text-blue-200 text-lg mr-3"></i>
            <input
              type="text"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              placeholder="ค้นหาชื่อกิจกรรม, สถานที่, หรือ #แท็ก"
              class="flex-1 bg-transparent border-none outline-none text-white text-lg placeholder-blue-200/70 h-12 font-medium"
            />
            <button 
              @click="handleSearch"
              class="bg-white hover:bg-blue-50 text-blue-900 px-8 py-3 rounded-full font-bold transition-all shadow-lg active:scale-95"
            >
              ค้นหา
            </button>
          </div>
        </div>

        <div class="flex justify-center mt-8">
          <button 
            @click="showAdvancedFilter = !showAdvancedFilter"
            class="text-sm font-medium text-blue-100 hover:text-white transition-colors flex items-center gap-2 bg-white/10 px-5 py-2.5 rounded-full border border-white/20 backdrop-blur-sm shadow-sm hover:bg-white/20"
          >
            <i :class="showAdvancedFilter ? 'fa-solid fa-chevron-up' : 'fa-solid fa-sliders'"></i>
            ตัวกรองเพิ่มเติม
            <span v-if="hasActiveFilters" class="bg-yellow-400 text-blue-900 text-[10px] px-1.5 py-0.5 rounded-full font-bold ml-1 shadow-sm">
              {{ getActiveFilterCount() }}
            </span>
          </button>
        </div>

        <div v-show="showAdvancedFilter" class="mt-4 bg-white/10 backdrop-blur-xl rounded-3xl p-6 border border-white/20 shadow-2xl animate-fade-in-down">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="form-group text-white">
              <label class="text-blue-100">หมวดหมู่</label>
              <select v-model="filters.category" @change="handleSearch" class="input-field-dark">
                <option value="">ทั้งหมด</option>
                <option value="academic">🎓 วิชาการ</option>
                <option value="technology">💻 เทคโนโลยี</option>
                <option value="entertainment">🎉 บันเทิง</option>
                <option value="sports">⚽ กีฬา</option>
                <option value="volunteer">🤝 จิตอาสา</option>
                <option value="career">💼 อาชีพ</option>
                <option value="other">📌 อื่นๆ</option>
              </select>
            </div>
            <div class="form-group text-white">
              <label class="text-blue-100">สถานะ</label>
              <select v-model="filters.status" @change="handleSearch" class="input-field-dark">
                <option value="">ทั้งหมด</option>
                <option value="กำลังรับสมัคร">🟢 กำลังรับสมัคร</option>
                <option value="กำลังดำเนินการ">🔵 กำลังดำเนินการ</option>
                <option value="สิ้นสุดแล้ว">🔴 สิ้นสุดแล้ว</option>
              </select>
            </div>
            <div class="form-group text-white">
              <label class="text-blue-100">เริ่มวันที่</label>
              <input type="date" v-model="filters.dateFrom" @change="handleSearch" class="input-field-dark"/>
            </div>
            <div class="col-span-1 md:col-span-3 flex justify-end">
              <button @click="clearFilters" class="text-sm text-red-300 hover:text-white hover:underline transition font-medium">
                ล้างค่าทั้งหมด
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="relative h-12 bg-[#F5F7FA] -mt-10 rounded-t-[3rem] z-20 shadow-[0_-10px_20px_rgba(0,0,0,0.05)]"></div>

    <div class="max-w-7xl mx-auto px-6 pb-24 pt-4">

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-24">
        <div class="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        <p class="mt-4 text-gray-500 font-medium animate-pulse">กำลังโหลดข้อมูล...</p>
      </div>

      <div v-else>
        
        <div v-if="recommendedList.length > 0 && isLoggedIn && !searchQuery && !hasActiveFilters" class="mb-12 relative">
          
          <div class="absolute inset-0 bg-gradient-to-r from-blue-50/50 via-indigo-50/30 to-transparent -mx-8 rounded-3xl -z-10"></div>

          <div class="flex items-center justify-between mb-6 pt-6">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-[#0071E3] to-[#00C7BE] text-white rounded-full flex items-center justify-center text-lg shadow-lg shadow-blue-200">
                 <i class="fa-solid fa-wand-magic-sparkles"></i>
              </div>
              <div>
                 <h2 class="text-2xl font-bold text-[#1D1D1F] tracking-tight">เลือกมาให้คุณ</h2>
                 <p class="text-gray-500 text-sm font-medium">กิจกรรมที่ตรงกับความสนใจของคุณที่สุด</p>
              </div>
            </div>
            
            <div class="hidden md:flex gap-2 text-gray-400">
               <i class="fa-solid fa-arrow-left-long"></i>
               <i class="fa-solid fa-arrow-right-long"></i>
            </div>
          </div>

          <div class="flex gap-6 overflow-x-auto pb-8 pt-2 -mx-2 px-2 snap-x snap-mandatory scrollbar-hide">
            <div
              v-for="(activity, index) in recommendedList" 
              :key="'rec-' + activity.id"
              @click="handleActivityClick(activity.id)"
              class="snap-center shrink-0 w-[280px] md:w-[320px] group bg-white rounded-[28px] shadow-[0_8px_24px_rgba(0,0,0,0.06)] hover:shadow-[0_20px_40px_rgba(0,113,227,0.15)] hover:-translate-y-2 transition-all duration-300 cursor-pointer overflow-hidden relative border border-white/60 flex flex-col h-full"
            >
               <div v-if="index === 0" class="absolute top-4 left-4 z-10 bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-[10px] font-bold px-3 py-1.5 rounded-full shadow-lg flex items-center gap-1.5 border border-white/20 tracking-wide uppercase">
                  <i class="fa-solid fa-crown"></i> แนะนำอันดับ 1
               </div>
               <div v-else-if="activity.matchScore > 0.8" class="absolute top-4 left-4 z-10 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-[10px] font-bold px-3 py-1.5 rounded-full shadow-lg flex items-center gap-1.5 border border-white/20 tracking-wide uppercase">
                  <i class="fa-solid fa-fire"></i> ตรงใจมาก
               </div>
               <div v-else class="absolute top-4 left-4 z-10 bg-white/90 backdrop-blur-md text-gray-700 text-[10px] font-bold px-3 py-1.5 rounded-full shadow-md border border-gray-100 tracking-wide uppercase">
                  <i class="fa-solid fa-thumbs-up text-blue-500"></i> น่าสนใจ
               </div>

               <div class="absolute top-4 right-4 z-10 bg-white/95 backdrop-blur-md text-[#0071E3] text-xs font-extrabold px-3 py-1.5 rounded-full shadow-sm flex items-center gap-1.5 border border-blue-100">
                  <i class="fa-solid fa-heart text-red-500"></i> {{ Math.round(activity.matchScore * 100) }}%
               </div>

               <div class="h-48 overflow-hidden bg-gray-100 relative">
                 <img :src="activity.image" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" @error="handleImageError">
                 <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-60"></div>
                 
                 <div class="absolute bottom-4 left-4 text-white text-xs font-bold px-2.5 py-1 rounded-lg bg-white/20 backdrop-blur-md border border-white/30">
                    {{ getCategoryLabel(activity.category) }}
                 </div>
               </div>
               
               <div class="p-5 flex flex-col flex-grow bg-white">
                 <h3 class="text-xl font-bold text-[#1D1D1F] line-clamp-2 mb-2 leading-snug group-hover:text-[#0071E3] transition-colors">{{ activity.title }}</h3>
                 
                 <div class="text-sm text-gray-500 mb-4 flex items-center gap-2 font-medium">
                    <i class="fa-regular fa-calendar-check text-[#0071E3]"></i> {{ activity.date }}
                 </div>

                 <div class="flex flex-wrap gap-1.5 mt-auto">
                    <span v-for="tag in activity.tags.slice(0, 2)" :key="tag" class="text-[10px] bg-gray-50 text-gray-600 px-2.5 py-1 rounded-md font-semibold border border-gray-100">#{{ tag }}</span>
                    <span v-if="activity.tags.length > 2" class="text-[10px] text-gray-400 px-1 py-1">+{{ activity.tags.length - 2 }}</span>
                 </div>
               </div>
            </div>
          </div>
          
          <div class="mt-8 border-t border-gray-200/60"></div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-8 px-2">
             <h2 class="text-2xl font-bold text-gray-900 tracking-tight flex items-center gap-3">
                <i v-if="searchQuery" class="fa-solid fa-magnifying-glass text-blue-600"></i>
                <i v-else class="fa-solid fa-layer-group text-blue-600"></i>
                {{ searchQuery || hasActiveFilters ? 'ผลการค้นหา' : 'กิจกรรมทั้งหมด' }}
                <span class="text-sm font-bold text-blue-600 bg-blue-50 border border-blue-100 px-3 py-1 rounded-full shadow-sm">
                  {{ activities.length }}
                </span>
             </h2>
          </div>

          <div v-if="activities.length === 0" class="text-center py-24 bg-white rounded-[32px] border border-dashed border-gray-200 shadow-sm">
             <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-300">
                <i class="fa-solid fa-search text-3xl"></i>
             </div>
             <h3 class="text-xl font-bold text-gray-900 mb-2">ไม่พบกิจกรรม</h3>
             <p class="text-gray-500 mb-6">ลองปรับเปลี่ยนคำค้นหาหรือตัวกรองดูใหม่</p>
             <button @click="clearFilters" class="text-blue-600 font-medium hover:underline">ล้างการค้นหา</button>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div
              v-for="activity in paginatedActivities"
              :key="activity.id"
              @click="handleActivityClick(activity.id)"
              class="group bg-white rounded-[24px] shadow-[0_4px_16px_rgba(0,0,0,0.04)] hover:shadow-[0_12px_30px_rgba(30,58,138,0.12)] hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden border border-gray-100 flex flex-col h-full"
            >
               <div class="h-52 overflow-hidden relative bg-gray-100">
                  <img :src="activity.image" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" @error="handleImageError">
                  <div class="absolute top-4 left-4 bg-white/90 backdrop-blur-sm text-gray-900 px-3 py-1 rounded-lg text-[11px] font-bold shadow-sm uppercase tracking-wide border border-gray-100">
                    {{ getCategoryLabel(activity.category) }}
                  </div>
               </div>
               
               <div class="p-6 flex flex-col flex-grow">
                  <h3 class="text-xl font-bold text-gray-900 mb-3 line-clamp-2 leading-snug group-hover:text-blue-700 transition-colors">{{ activity.title }}</h3>
                  
                  <div class="space-y-2 text-sm text-gray-500 mb-6 flex-grow">
                    <div class="flex items-center gap-3">
                        <i class="fa-regular fa-calendar w-5 text-center text-blue-500"></i>
                        <span>{{ activity.date }}</span>
                    </div>
                    <div class="flex items-center gap-3">
                        <i class="fa-regular fa-clock w-5 text-center text-blue-500"></i>
                        <span>{{ activity.time }}</span>
                    </div>
                  </div>

                  <div class="pt-5 border-t border-gray-50 mt-auto flex items-center justify-between">
                    <span 
                      class="text-[11px] font-bold px-3 py-1 rounded-full border" 
                      :class="getStatusClass(activity.status)"
                    >
                      {{ activity.status }}
                    </span>
                    <div class="w-9 h-9 rounded-full bg-blue-50 flex items-center justify-center text-blue-500 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-sm">
                      <i class="fa-solid fa-arrow-right text-xs"></i>
                    </div>
                  </div>
               </div>
            </div>
          </div>

          <div v-if="totalPages > 1" class="flex justify-center mt-16">
            <div class="flex items-center gap-2 bg-white px-2 py-2 rounded-full shadow-lg border border-gray-200">
              <button 
                @click="changePage(currentPage - 1)" 
                :disabled="currentPage === 1" 
                class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed transition"
              >
                <i class="fa-solid fa-chevron-left text-sm"></i>
              </button>
              
              <div class="px-4 text-sm font-medium text-gray-600">
                <span class="text-blue-700 font-bold text-lg">{{ currentPage }}</span> / {{ totalPages }}
              </div>
              
              <button 
                @click="changePage(currentPage + 1)" 
                :disabled="currentPage === totalPages" 
                class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed transition"
              >
                <i class="fa-solid fa-chevron-right text-sm"></i>
              </button>
            </div>
          </div>

        </div>
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
import { ref, computed, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import activityService from "@/services/activityService.js"
import notificationService from "@/services/notificationService.js"
import authService from "@/services/authService.js"
import OnboardingModal from "./OnboardingModal.vue" 

const router = useRouter()

// State
const searchQuery = ref("")
const recommendedList = ref([]) 
const activities = ref([]) 
const isLoggedIn = ref(false)
const isLoading = ref(false)
const showDropdown = ref(false)
const showNotificationDropdown = ref(false)
const showAdvancedFilter = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const organizerStatus = ref('none')
const userProfile = ref(null)

const filters = ref({
  category: "", dateFrom: "", dateTo: "", tag: "", status: ""
})

const showToast = ref(false)
const toastMessage = ref("")
const toastClass = ref("bg-[#1E3A8A]")

// Computed
const hasActiveFilters = computed(() => {
  return filters.value.category || filters.value.dateFrom || 
         filters.value.dateTo || filters.value.tag || filters.value.status
})

const itemsPerPage = 12
const currentPage = ref(1)

const paginatedActivities = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return activities.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(activities.value.length / itemsPerPage))

// Functions
const triggerToast = (message, type = "info") => {
  toastClass.value = { 
    info: "bg-[#1E3A8A]", 
    success: "bg-[#10B981]", 
    error: "bg-[#EF4444]" 
  }[type] || "bg-[#1E3A8A]"
  
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => (showToast.value = false), 2500)
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: "smooth" })
  }
}

const checkLoginStatus = async () => {
  isLoggedIn.value = !!localStorage.getItem("access")
  if (isLoggedIn.value) {
      organizerStatus.value = localStorage.getItem('organizer_status') || 'none'
      try {
          const res = await authService.getUserProfile()
          organizerStatus.value = res.data.organizer_status || 'none'
          localStorage.setItem('organizer_status', organizerStatus.value)
          
          userProfile.value = res.data
          console.log('✅ [Home] Profile loaded:', res.data.username)
          console.log('✅ [Home] Profile Image:', res.data?.profile?.profile_image)
      } catch (e) {
          if (e.response?.status === 401) handleLogout()
      }
  } else {
      userProfile.value = null
  }
}

// ⭐ แก้ไขใหม่: ให้ redirect ไปหน้า RequestOrganizer แทนการยิง API
const requestOrganizer = () => {
  closeDropdown()
  router.push('/request-organizer')
}

const handleLogout = async () => {
  localStorage.clear()
  isLoggedIn.value = false
  showDropdown.value = false
  showNotificationDropdown.value = false
  recommendedList.value = [] 
  notifications.value = []
  unreadCount.value = 0
  
  triggerToast("ออกจากระบบเรียบร้อยแล้ว", "success")
  
  await fetchActivities() 
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

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
  if (!e.target.closest('.relative')) closeDropdown() 
}

// Notification Logic
const fetchNotifications = async () => {
  if (!isLoggedIn.value) return
  try {
    const res = await notificationService.getMyNotifications()
    const data = Array.isArray(res.data) ? res.data : (res.data.results || [])
    notifications.value = data
    unreadCount.value = data.filter(n => !n.is_read).length
  } catch (e) {
    console.error("Noti error:", e)
    notifications.value = []
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

// Data Helpers
const getTags = (a) => {
  if (a.tag_list?.length) return a.tag_list.map(t => t.name)
  if (a.tags) return a.tags.split(",")
  return ["กิจกรรม"]
}

const mapActivityData = (a, isRec = false) => ({
  id: a.id,
  title: a.name,
  date: formatDate(a.date),
  time: a.time_display || a.time || "ไม่ระบุ",
  tags: getTags(a),
  image: a.image || "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400",
  category: a.category,
  status: a.status,
  isRecommended: isRec,
  matchScore: a.match_score || 0
})

const getCategoryLabel = (cat) => {
  const map = { academic: "วิชาการ", technology: "เทคโนโลยี", entertainment: "บันเทิง", sports: "กีฬา", volunteer: "จิตอาสา", career: "อาชีพ", other: "ทั่วไป" }
  return map[cat] || cat
}

const getStatusClass = (status) => {
  if (status === 'กำลังรับสมัคร') return 'bg-green-50 text-green-700 border-green-200'
  if (status === 'กำลังดำเนินการ') return 'bg-blue-50 text-blue-700 border-blue-200'
  return 'bg-gray-100 text-gray-500 border-gray-200'
}

const formatDate = d => {
  if (!d) return "-"
  return new Date(d).toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: '2-digit' })
}

const handleImageError = (e) => { e.target.src = "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400" }
const handleActivityClick = id => router.push(`/activity/${id}`)
const handleSearch = () => { fetchActivities() }
const clearFilters = () => { 
  searchQuery.value = ""
  filters.value = { category: "", dateFrom: "", dateTo: "", tag: "", status: "" }
  fetchActivities()
}
const getActiveFilterCount = () => {
  let count = 0
  if (filters.value.category) count++
  if (filters.value.dateFrom) count++
  if (filters.value.dateTo) count++
  if (filters.value.tag) count++
  if (filters.value.status) count++
  return count
}

// API Call
const fetchActivities = async () => {
  try {
    isLoading.value = true
    
    if (searchQuery.value || hasActiveFilters.value) {
      const params = {
        search: searchQuery.value,
        category: filters.value.category,
        date_from: filters.value.dateFrom,
        date_to: filters.value.dateTo,
        tag: filters.value.tag,
        status: filters.value.status
      }
      const res = await activityService.getAllActivities(params)
      const results = Array.isArray(res.data) ? res.data : (res.data.results || [])
      activities.value = results.map(a => mapActivityData(a))
      recommendedList.value = []
    } else {
      if (isLoggedIn.value) {
          try {
            const recRes = await activityService.getRecommendedActivities()
            if (recRes.data.recommendation_type === 'personalized') {
               recommendedList.value = (recRes.data.activities || []).map(a => mapActivityData(a, true))
            } else {
               recommendedList.value = []
            }
          } catch (e) {
            console.warn("Failed to load recommended activities")
          }
      } else {
          recommendedList.value = []
      }

      const allRes = await activityService.getAllActivities()
      const allResults = Array.isArray(allRes.data) ? allRes.data : (allRes.data.results || [])
      activities.value = allResults.map(a => mapActivityData(a))
    }
    
    currentPage.value = 1
  } catch (error) {
    console.error("Fetch error:", error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  checkLoginStatus()
  fetchActivities()
  if (isLoggedIn.value) {
    fetchNotifications()
    setInterval(fetchNotifications, 30000) // Poll notification
  }
  window.addEventListener("storage", checkLoginStatus)
  document.addEventListener("click", handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener("storage", checkLoginStatus)
  document.removeEventListener("click", handleClickOutside)
})
</script>

<style>
/* Font Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
</style>

<style scoped>
/* Scoped Styles */
.font-sans {
  font-family: 'Inter', sans-serif;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.animate-fade-in-up { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; }
.animate-fade-in-down { animation: fadeInDown 0.3s ease-out forwards; }
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }
.animate-pulse-slow { animation: pulseSlow 6s infinite; }

@keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
@keyframes pulseSlow { 0%, 100% { opacity: 0.2; transform: scale(1); } 50% { opacity: 0.3; transform: scale(1.05); } }

.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }

/* Custom Inputs (Dark Style for Hero Section) */
.form-group label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.input-field-dark {
  width: 100%;
  padding: 0.6rem 1rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  font-size: 0.9rem;
  color: white;
  outline: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.2s;
}

.input-field-dark:focus {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: white;
}

.input-field-dark option {
  background-color: #1E3A8A;
  color: white;
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

/* Scrollbar Hide for Horizontal List */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>