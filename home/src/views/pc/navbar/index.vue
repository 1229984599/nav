<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import MProfile from "@/components/MProfile.vue";
import MWeather from "@/components/weather/index.vue";
import MYiyan from "@/components/MYiyan.vue";
import { useSiteStore } from "@/store/site";
import { useAppStore } from "@/store/app";
import MHot from "@/components/hot/index.vue";
import { isMobile } from "@/utils/window";
import { useTheme } from "@/composables/useTheme";
import { computed } from "vue";

defineOptions({
  name: "MNavbar",
});

const emit = defineEmits<{
  (e: "open-search"): void;
}>();

const appStore = useAppStore();
const siteStore = useSiteStore();
const { themeMode, toggleTheme } = useTheme();

const themeIcon = computed(() => {
  if (themeMode.value === "dark") return "mdi:weather-night";
  if (themeMode.value === "light") return "mdi:white-balance-sunny";
  return "mdi:theme-light-dark";
});

const themeTitle = computed(() => {
  if (themeMode.value === "dark") return "暗色模式（点击切换）";
  if (themeMode.value === "light") return "亮色模式（点击切换）";
  return "跟随系统（点击切换）";
});
</script>

<template>
  <div class="nav_container">
    <!--    左侧小组件-->
    <div class="nav-left-container">
      <!--    菜单按钮-->
      <m-icon
        size="45"
        @click.stop="appStore.toggleSlide()"
        class="cursor-pointer hover:text-sky-800 dark:hover:text-sky-300 transition-colors"
        icon="ph:list-fill"
      />
      <!--      今日热榜-->
      <m-hot />
      <!--      天气-->
      <m-weather v-if="siteStore.siteInfo?.weather" />
    </div>

    <div class="nav-right-container">
      <m-yiyan v-if="siteStore.siteInfo?.yiyan" />
      <div></div>
      <div class="flex items-center gap-x-2">
        <m-icon
          :icon="themeIcon"
          :size="22"
          class="cursor-pointer hover:text-sky-800 dark:hover:text-sky-300 transition-colors"
          :title="themeTitle"
          @click="toggleTheme"
        />
        <m-icon
          v-if="isMobile"
          icon="mingcute:search-line"
          :size="24"
          class="cursor-pointer hover:text-sky-800 dark:hover:text-sky-300 transition-colors"
          @click="emit('open-search')"
        />
        <m-profile class="mr-1" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.nav_container {
  display: flex;
  align-items: center;
  justify-content: space-between;

  .nav-left-container {
    display: flex;
    flex-shrink: 0;
    column-gap: 2px;
    align-items: center;
  }

  .nav-right-container {
    display: flex;
    align-items: center;
    width: 65%;
    justify-content: space-between;

    & > span:first-child {
      flex-basis: 80%;
    }
  }
}
</style>
