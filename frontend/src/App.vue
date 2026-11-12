<template>
  <router-view />
  <PopupAnnouncement />   <!-- เพิ่มบรรทัดนี้ -->
</template>

<script setup>
import PopupAnnouncement from "@/components/PopupAnnouncement.vue";   // เพิ่มบรรทัดนี้
// ไม่ต้อง import อะไร Vue Router จะจัดการเองจะจัดการเอง
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
}
</style>