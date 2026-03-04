<script setup lang="ts">
import MMobileHeader from "./header/index.vue";
import MMobileMain from "./main/index.vue";
import MMobileFooter from "./footer/index.vue";
import { computed } from "vue";
import { useAppStore } from "@/store/app";

const appStore = useAppStore();
const bgUrl = computed(() => {
  return `url(${appStore.bgUrl})`;
});
</script>

<template>
  <div class="mobile-container">
    <div class="mobile-mask"></div>
    <div class="mobile-shell">
      <m-mobile-header />
      <m-mobile-main />
    </div>
    <m-mobile-footer />
  </div>
</template>

<style scoped lang="scss">
.mobile-container {
  position: relative;
  box-sizing: border-box;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-image: v-bind(bgUrl);
  background-size: cover;
  background-position: center;
}

.mobile-mask {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 10% 6%, rgba(255, 255, 255, 0.55), transparent 34%),
    radial-gradient(circle at 84% 14%, rgba(127, 182, 255, 0.24), transparent 32%),
    linear-gradient(160deg, rgba(16, 21, 33, 0.18), rgba(9, 12, 18, 0.34));
  backdrop-filter: saturate(1.2) brightness(1.03);
}

.mobile-shell {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding-bottom: 112px;
}
</style>
