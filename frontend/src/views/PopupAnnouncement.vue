<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useRoute } from "vue-router";
import { getActivePopups, getPopupPreview } from "@/services/popupService";

const route = useRoute();
const popup = ref(null);
const isPreview = ref(false);
const fading = ref(false);
let fadeTimer = null;
let removeTimer = null;
let delayTimer = null;
let pending = false;
let alive = true;

// หน้าที่ไม่ให้ popup ขึ้น
const HIDDEN_PATHS = ["/login", "/register", "/forgot-password"];

const isInternal = computed(() => popup.value?.link_url?.startsWith("/"));

const safe = (fn, fallback = null) => { try { return fn(); } catch { return fallback; } };

const isLoggedIn = () => !!safe(() => localStorage.getItem("access"));

const getDismissed = () =>
  safe(() => JSON.parse(localStorage.getItem("popup-dismissed") || "[]"), []);

function clearTimers() { clearTimeout(fadeTimer); clearTimeout(removeTimer); }

function startFade() {
  clearTimers();
  const s = popup.value?.auto_close_seconds;
  if (s > 0) {
    fadeTimer = setTimeout(() => {
      fading.value = true;
      removeTimer = setTimeout(close, 400);
    }, s * 1000);
  }
}

function pause() { clearTimers(); fading.value = false; }

function show(p) { popup.value = p; startFade(); }

function close() {
  clearTimers();
  if (!isPreview.value) safe(() => sessionStorage.setItem("popup-closed", "1"));
  popup.value = null;
  fading.value = false;
}

function dismissForever() {
  if (!isPreview.value && popup.value) {
    const list = getDismissed();
    if (!list.includes(popup.value.id)) list.push(popup.value.id);
    safe(() => localStorage.setItem("popup-dismissed", JSON.stringify(list)));
  }
  close();
}

async function tryShow() {
  if (popup.value || pending) return;
  pending = true;
  try {
    const previewToken = route.query.popup_preview;
    if (previewToken) {
      isPreview.value = true;
      show(await getPopupPreview(previewToken));
      return;
    }
    if (!isLoggedIn() || HIDDEN_PATHS.includes(route.path)) return;
    if (safe(() => sessionStorage.getItem("popup-closed"))) return;

    const dismissed = getDismissed();
    const next = (await getActivePopups()).find((p) => !dismissed.includes(p.id));
    if (!next) return;

    await new Promise((resolve) => {
      delayTimer = setTimeout(resolve, (next.delay_seconds ?? 3) * 1000);
    });
    if (alive && isLoggedIn() && !popup.value && !HIDDEN_PATHS.includes(route.path)) {
      show(next);
    }
  } catch {
    /* เงียบไว้ */
  } finally {
    pending = false;
  }
}

function onKey(e) { if (e.key === "Escape" && popup.value) close(); }

onMounted(() => {
  window.addEventListener("keydown", onKey);
  tryShow();
});

watch(() => route.fullPath, tryShow);

onBeforeUnmount(() => {
  alive = false;
  window.removeEventListener("keydown", onKey);
  clearTimers();
  clearTimeout(delayTimer);
});
</script>

<template>
  <div v-if="popup" class="popup-backdrop" :class="{ fading }" @click="close">
    <div class="popup-card" role="dialog" aria-modal="true" :aria-label="popup.title"
         @click.stop @mouseenter="pause" @mouseleave="startFade">
      
      <!-- ปุ่มปิดดีไซน์ใหม่ มินิมอล วางมุมขวาบนของการ์ด -->
      <button class="popup-close" aria-label="ปิด" @click="close">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>

      <span v-if="isPreview" class="popup-badge">โหมดพรีวิว (ยังไม่เผยแพร่)</span>

      <div class="popup-scroll">
        <div v-if="popup.image" class="popup-image-container">
          <router-link v-if="popup.link_url && isInternal" :to="popup.link_url" @click="close">
            <img :src="popup.image" :alt="popup.title" />
          </router-link>
          <a v-else-if="popup.link_url" :href="popup.link_url" target="_blank" rel="noopener noreferrer">
            <img :src="popup.image" :alt="popup.title" />
          </a>
          <img v-else :src="popup.image" :alt="popup.title" />
        </div>

        <div class="popup-content">
          <h3>{{ popup.title }}</h3>
          <p>{{ popup.message }}</p>
        </div>
      </div>

      <div class="popup-footer">
        <button class="popup-dismiss" @click="dismissForever">ไม่ต้องแสดงอีก</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.popup-backdrop {
  position: fixed; top: 0; left: 0; z-index: 1000;
  width: 100%;
  height: 100vh;
  height: 100dvh;
  display: flex; align-items: center; justify-content: center;
  padding: 16px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  transition: opacity 0.3s ease;
}
.popup-backdrop.fading { opacity: 0; pointer-events: none; }

.popup-card {
  position: relative;
  display: flex; flex-direction: column;
  width: min(100%, 420px);
  max-height: 90vh;
  max-height: 90dvh;
  background: #ffffff; 
  border-radius: 20px; 
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  animation: popupScaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes popupScaleUp {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.popup-scroll {
  flex: 1 1 auto; min-height: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}

.popup-image-container {
  width: 100%;
  background: #f8fafc;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-scroll img {
  display: block; width: 100%; height: auto;
  max-height: 50vh;
  object-fit: cover;
}

.popup-content {
  padding: 20px 24px 8px;
}

.popup-scroll h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem; 
  font-weight: 700;
  line-height: 1.4; 
  color: #0f172a;
  overflow-wrap: anywhere;
}

.popup-scroll p {
  margin: 0;
  white-space: pre-line;
  font-size: 0.95rem; 
  line-height: 1.6; 
  color: #475569;
  overflow-wrap: anywhere;
}

.popup-footer {
  padding: 12px 24px 20px;
  display: flex;
  justify-content: center;
  background: #ffffff;
}

.popup-close {
  position: absolute; top: 12px; right: 12px; z-index: 10;
  width: 32px; height: 32px;
  border: none; border-radius: 50%;
  background: rgba(255, 255, 255, 0.85); 
  color: #475569;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}
.popup-close:hover {
  background: #ffffff;
  color: #0f172a;
  transform: scale(1.05);
}

.popup-badge {
  position: absolute; top: 12px; left: 12px; z-index: 10;
  background: rgba(245, 158, 11, 0.9); backdrop-filter: blur(4px);
  color: #fff; font-size: 11px; font-weight: 600;
  padding: 4px 10px; border-radius: 999px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.popup-dismiss {
  background: none; border: 0;
  color: #94a3b8; font-size: 0.875rem;
  text-decoration: underline; cursor: pointer;
  transition: color 0.2s;
}
.popup-dismiss:hover {
  color: #64748b;
}

/* มือถือแนวนอน / จอเตี้ย */
@media (max-height: 480px) {
  .popup-scroll img { max-height: 35vh; }
  .popup-content { padding: 14px 20px 4px; }
  .popup-footer { padding: 8px 20px 14px; }
}
</style>