<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import MProfile from "@/views/pc/navbar/MProfile.vue";
import MWeather from "./weather/index.vue";
import MYiyan from "./MYiyan.vue";
import { useSiteStore } from "@/store/site";
import { useAppStore } from "@/store/app";
import { isMobile } from "@/utils/window";
import MHot from "./hot/index.vue";
defineOptions({
  name: "MNavbar",
});
const appStore = useAppStore();
const siteStore = useSiteStore();
</script>

<template>
  <div class="nav_container">
    <!--    左侧小组件-->
    <div class="nav-left-container">
      <!--    菜单按钮-->
      <m-icon
        size="45"
        @click.stop="appStore.toggleSlide()"
        class="cursor-pointer px-1 hover:text-sky-800 transition-colors"
        icon="ph:list-fill"
      />
      <!--      今日热榜-->
      <m-hot />
      <!--      天气-->
      <m-weather v-if="!isMobile && siteStore.siteInfo?.weather" />
    </div>

    <div class="nav-right-container">
      <m-yiyan v-if="siteStore.siteInfo?.yiyan" />
      <!--      占位，防止个人中心到最前面-->
      <div></div>
      <m-profile class="mr-1" />
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
