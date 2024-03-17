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
    <m-mobile-header />
    <m-mobile-main />
    <m-mobile-footer />
  </div>
</template>

<style scoped lang="scss">
.mobile-container {
  box-sizing: border-box;
  width: 100vw;
  height: 100vh;
  background-image: v-bind(bgUrl);
  background-size: cover;
  background-position: center;
}
</style>
