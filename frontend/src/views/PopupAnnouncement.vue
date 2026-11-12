<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRoute } from "vue-router";
import { getActivePopups, getPopupPreview } from "@/services/popupService";

const route = useRoute();
const popup = ref(null);
const isPreview = ref(false);
const fading = ref(false);
let fadeTimer = null;
let removeTimer = null;

const isInternal = computed(() => popup.value?.link_url?.startsWith("/"));

const safe = (fn, fallback = null) => { try { return fn(); } catch { return fallback; } };
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

function onKey(e) { if (e.key === "Escape" && popup.value) close(); }

onMounted(async () => {
  window.addEventListener("keydown", onKey);
  try {
    const token = route.query.popup_preview;
    if (token) {                                        // โหมดพรีวิวของแอดมิน
      isPreview.value = true;
      show(await getPopupPreview(token));
      return;
    }
    if (safe(() => sessionStorage.getItem("popup-closed"))) return;   // เข้ารอบนี้ปิดไปแล้ว
    const dismissed = getDismissed();
    const next = (await getActivePopups()).find((p) => !dismissed.includes(p.id));
    if (next) show(next);
  } catch {}
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKey);
  clearTimers();
});
</script>

<template>
  <div v-if="popup" class="popup-backdrop" :class="{ fading }" @click="close">
    <div class="popup-card" @click.stop @mouseenter="pause" @mouseleave="startFade">
      <span v-if="isPreview" class="popup-badge">โหมดพรีวิว (ยังไม่เผยแพร่)</span>
      <button class="popup-close" aria-label="ปิด" @click="close">×</button>

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
      <button class="popup-dismiss" @click="dismissForever">ไม่ต้องแสดงอีก</button>
    </div>
  </div>
</template>

<style scoped>
.popup-backdrop {
  position: fixed; inset: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: center;
  padding: 16px;
  background: rgba(0, 0, 0, 0.55);
  transition: opacity 0.6s ease;
}
.popup-backdrop.fading { opacity: 0; pointer-events: none; }

.popup-card {
  position: relative;
  width: min(90vw, 440px);
  max-height: 85vh; overflow-y: auto;
  background: #fff; border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}
.popup-card img {
  display: block; width: 100%; height: auto;
  border-radius: 16px 16px 0 0;
}
.popup-card h3, .popup-card p { margin: 0; padding: 12px 16px 0; }
.popup-card p { padding-bottom: 16px; white-space: pre-line; }

.popup-close {
  position: absolute; top: 8px; right: 8px; z-index: 2;
  width: 40px; height: 40px;
  border: 0; border-radius: 50%;
  background: rgba(0, 0, 0, 0.55); color: #fff;
  font-size: 22px; cursor: pointer;
}
.popup-badge {
  position: absolute; top: 8px; left: 8px; z-index: 2;
  background: #f59e0b; color: #fff; font-size: 12px;
  padding: 2px 8px; border-radius: 999px;
}
.popup-dismiss {
  display: block; margin: 0 auto; padding: 4px 16px 16px;
  background: none; border: 0;
  color: #6b7280; font-size: 13px;
  text-decoration: underline; cursor: pointer;
}
</style>