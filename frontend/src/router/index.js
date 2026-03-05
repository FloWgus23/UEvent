// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import OrganizerDashboard from '../views/OrganizerDashboard.vue'
import CreateActivity from '../views/CreateActivity.vue'
import CreateNews from '../views/CreateNews.vue'
import EditActivity from '../views/EditActivity.vue'
import EditNews from '../views/EditNews.vue'
import News from '../views/News.vue'
import Category from '../views/Category.vue'
import Profile from '../views/Profile.vue'
import Notification from '../views/Notification.vue'
import ActivityDetail from '../views/ActivityDetail.vue'
import MyActivities from '../views/MyActivities.vue'
import ActivityRegistrations from '../views/ActivityRegistrations.vue'
import UserDashboard from '../views/UserDashboard.vue'
import RequestOrganizer from '../views/RequestOrganizer.vue'
import WaitingForApproval from '../views/WaitingForApproval.vue'
import ForgotPassword from '../views/ForgotPassword.vue' 

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  
  // หน้าลืมรหัสผ่าน
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword },

  // หน้า News
  { path: '/news', name: 'News', component: News },

  // หน้า News Detail
  {
    path: '/news/:id',
    name: 'NewsDetail',
    component: () => import('../views/NewsDetail.vue'),
    props: true
  },

  { path: '/category', name: 'Category', component: Category },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/notifications', name: 'Notification', component: Notification, meta: { requiresAuth: true } },
  { path: '/activity/:id', name: 'ActivityDetail', component: ActivityDetail },

  {
    path: '/profile/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/activities',
    name: 'MyActivities',
    component: MyActivities,
    meta: { requiresAuth: true }
  },

  // Route สำหรับการขอเป็นผู้จัด
  { 
    path: '/request-organizer', 
    name: 'RequestOrganizer', 
    component: RequestOrganizer,
    meta: { requiresAuth: true } 
  },
  
  // Route สำหรับหน้ารออนุมัติ
  { 
    path: '/waiting-approval', 
    name: 'WaitingForApproval', 
    component: WaitingForApproval,
    meta: { requiresAuth: true } 
  },

  // โซนผู้จัดกิจกรรม (Organizer)
  {
    path: '/organizer/dashboard',
    name: 'OrganizerDashboard',
    component: OrganizerDashboard,
    meta: { requiresOrganizer: true }
  },
  {
    path: '/organizer/create-activity',
    name: 'CreateActivity',
    component: CreateActivity,
    meta: { requiresOrganizer: true }
  },
  {
    path: '/organizer/create-news',
    name: 'CreateNews',
    component: CreateNews,
    meta: { requiresOrganizer: true }
  },
  {
    path: '/organizer/edit-activity/:id',
    name: 'EditActivity',
    component: EditActivity,
    props: true,
    meta: { requiresOrganizer: true }
  },
  {
    path: '/organizer/edit-news/:id',
    name: 'EditNews',
    component: EditNews,
    props: true,
    meta: { requiresOrganizer: true }
  },
  {
    path: '/organizer/activity/:id/registrations',
    name: 'ActivityRegistrations',
    component: ActivityRegistrations,
    meta: { requiresOrganizer: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem("access")
  const organizerStatus = localStorage.getItem("organizer_status") // 'none', 'pending', 'approved'

  // 1. เช็คว่าต้องเป็นผู้จัด (Organizer) หรือไม่
  if (to.matched.some(record => record.meta.requiresOrganizer)) {
    if (!isLoggedIn) {
      alert("กรุณาเข้าสู่ระบบก่อนครับ")
      return next("/login")
    }
    
    if (organizerStatus !== 'approved') {
      alert("คุณไม่มีสิทธิ์เข้าถึงส่วนผู้จัดกิจกรรม (ต้องได้รับอนุมัติก่อน)")
      return next("/")
    }
  }

  // 2. เช็คว่าต้อง Login ทั่วไปหรือไม่
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      alert("กรุณาเข้าสู่ระบบก่อนครับ")
      return next("/login")
    }
  }

  // 3. ถ้าเป็นหน้า Login/Register หรือ ForgotPassword แต่ Login อยู่แล้ว ให้ดีดไปหน้าแรก
  // เพิ่ม forgot-password เข้าไปในเงื่อนไขด้วย เพื่อไม่ให้คนที่ล็อกอินแล้วเข้าหน้านี้ได้
  if ((to.path === '/login' || to.path === '/register' || to.path === '/forgot-password') && isLoggedIn) {
    return next("/")
  }

  next()
})

export default router