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

// หน้าที่ไม่ให้ popup ขึ้น ปรับให้ตรงกับ router ของคุณ
const HIDDEN_PATHS = ["/login", "/register"];

const isInternal = computed(() => popup.value?.link_url?.startsWith("/"));

const safe = (fn, fallback = null) => { try { return fn(); } catch { return fallback; } };

// ปรับให้ตรงกับชื่อที่โปรเจคคุณเก็บ token ล็อกอิน
const isLoggedIn = () =>
  !!(safe(() => localStorage.getItem("access_token")) ||
     safe(() => localStorage.getItem("token")));

const getDismissed = () =>
  safe(() => JSON.parse(localStorage.getItem("popup-dismissed") || "[]"), []);

function clearTimers() { clearTimeout(fadeTimer); clearTimeout(removeTimer); }

function startFade() {
  clearTimers();
  const s = popup.value?.auto_close_seconds;
  if (s > 0) {
    fadeTimer = setTimeout(() => {
      fading.value = true;
      removeTimer = setTimeout(close, 600);   // ตรงกับเวลา transition ใน CSS
    }, s * 1000);
  }
}

function pause() { clearTimers(); fading.value = false; }

function show(p) { popup.value = p; startFade(); }

function close() {                       // กด × / กดพื้นหลัง / จางหายเอง
  clearTimers();
  if (!isPreview.value) safe(() => sessionStorage.setItem("popup-closed", "1"));
  popup.value = null;
  fading.value = false;
}

function dismissForever() {              // ไม่ต้องแสดงอีก
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
    if (previewToken) {                                  // โหมดพรีวิวของแอดมิน: ขึ้นทันที
      isPreview.value = true;
      show(await getPopupPreview(previewToken));
      return;
    }
    if (!isLoggedIn() || HIDDEN_PATHS.includes(route.path)) return;
    if (safe(() => sessionStorage.getItem("popup-closed"))) return;

    const dismissed = getDismissed();
    const next = (await getActivePopups()).find((p) => !dismissed.includes(p.id));
    if (!next) return;

    await new Promise((resolve) => {                     // รอตามที่แอดมินตั้งไว้
      delayTimer = setTimeout(resolve, (next.delay_seconds ?? 3) * 1000);
    });
    if (alive && isLoggedIn() && !popup.value && !HIDDEN_PATHS.includes(route.path)) {
      show(next);
    }
  } catch {
    /* เงียบไว้ ไม่ให้ popup ทำให้หน้าเว็บพัง */
  } finally {
    pending = false;
  }
}

function onKey(e) { if (e.key === "Escape" && popup.value) close(); }

onMounted(() => {
  window.addEventListener("keydown", onKey);
  tryShow();
});

// เปลี่ยนหน้า (รวมถึงหลังล็อกอินแล้วระบบพาไปหน้าอื่น) ให้เช็คใหม่
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
      <span v-if="isPreview" class="popup-badge">โหมดพรีวิว (ยังไม่เผยแพร่)</span>
      <button class="popup-close" aria-label="ปิด" @click="close">×</button>

      <div class="popup-scroll">
        <router-link v-if="popup.image && popup.link_url && isInternal"
                     :to="popup.link_url" @click="close">
          <img :src="popup.image" :alt="popup.title" />
        </router-link>
        <a v-else-if="popup.image && popup.link_url" :href="popup.link_url"
           target="_blank" rel="noopener noreferrer">
          <img :src="popup.image" :alt="popup.title" />
        </a>
        <img v-else-if="popup.image" :src="popup.image" :alt="popup.title" />

        <h3>{{ popup.title }}</h3>
        <p>{{ popup.message }}</p>
      </div>

      <button class="popup-dismiss" @click="dismissForever">ไม่ต้องแสดงอีก</button>
    </div>
  </div>
</template>

<style scoped>
.popup-backdrop {
  position: fixed; top: 0; left: 0; z-index: 1000;
  width: 100%;
  height: 100vh;
  height: 100dvh;                       /* ความสูงจอจริงบนมือถือ */
  display: flex; align-items: center; justify-content: center;
  padding: max(12px, env(safe-area-inset-top)) max(12px, env(safe-area-inset-right))
           max(12px, env(safe-area-inset-bottom)) max(12px, env(safe-area-inset-left));
  background: rgba(0, 0, 0, 0.55);
  transition: opacity 0.6s ease;
}
.popup-backdrop.fading { opacity: 0; pointer-events: none; }

.popup-card {
  position: relative;
  display: flex; flex-direction: column;
  width: min(100%, 440px);
  max-height: 100%;                     /* ไม่เกินความสูงจอเสมอ */
  background: #fff; border-radius: 16px; overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.popup-scroll {
  flex: 1 1 auto; min-height: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}
.popup-scroll img {
  display: block; width: 100%; height: auto;
  max-height: 60vh;
  max-height: 60dvh;                    /* รูปสูงไม่เกิน 60% ของจอ */
  object-fit: contain;
  background: #f3f4f6;
}
.popup-scroll h3,
.popup-scroll p {
  margin: 0; padding: 12px 16px 0;
  overflow-wrap: anywhere;              /* คำยาวหรือลิงก์ยาวไม่ดันกล่องให้ล้น */
}
.popup-scroll p { padding-bottom: 12px; white-space: pre-line; }

.popup-close {
  position: absolute; top: 8px; right: 8px; z-index: 2;
  width: 44px; height: 44px;            /* ขนาดพอให้นิ้วกดง่าย */
  border: 0; border-radius: 50%;
  background: rgba(0, 0, 0, 0.55); color: #fff;
  font-size: 24px; line-height: 1; cursor: pointer;
}
.popup-badge {
  position: absolute; top: 8px; left: 8px; z-index: 2;
  background: #f59e0b; color: #fff; font-size: 12px;
  padding: 2px 8px; border-radius: 999px;
}
.popup-dismiss {
  flex: none;
  padding: 10px 16px 14px;
  background: none; border: 0;
  color: #6b7280; font-size: 13px;
  text-decoration: underline; cursor: pointer;
}

/* มือถือแนวนอน / จอเตี้ย */
@media (max-height: 480px) {
  .popup-scroll img { max-height: 45vh; max-height: 45dvh; }
  .popup-scroll h3, .popup-scroll p { padding-top: 8px; }
  .popup-dismiss { padding: 6px 16px 10px; }
}

/* จอใหญ่ */
@media (min-width: 1600px) {
  .popup-card { width: min(100%, 520px); }
}
</style>