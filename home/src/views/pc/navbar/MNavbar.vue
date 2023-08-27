<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import MProfile from "@/views/pc/navbar/MProfile.vue";
import MWeather from "@/components/MWeather.vue";
import MYiyan from "@/components/MYiyan.vue";
import { useSiteStore } from "@/store/site";
import { useAppStore } from "@/store/app";

const appStore = useAppStore();
const siteStore = useSiteStore();
</script>

<template>
  <div class="flex items-center justify-between">
    <m-icon
      @click="appStore.toggleSlide()"
      class="cursor-pointer px-2"
      icon="ph:list-fill"
    />
    <m-weather v-if="siteStore.siteInfo?.weather" />
    <div class="w-4/5 flex items-center justify-between">
      <!--      占位，防止一言到最前面-->
      <span></span>
      <m-yiyan v-if="siteStore.siteInfo?.yiyan" />
      <m-profile class="mr-1" />
    </div>
  </div>
</template>

<style scoped></style>
