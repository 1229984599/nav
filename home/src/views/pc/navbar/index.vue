<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import MProfile from "@/views/pc/navbar/MProfile.vue";
import MWeather from "./MWeather.vue";
import MYiyan from "./MYiyan.vue";
import { useSiteStore } from "@/store/site";
import { useAppStore } from "@/store/app";
import { isMobile } from "@/utils/window";
import MHot from "@/views/pc/navbar/MHot.vue";
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
        @click="appStore.toggleSlide()"
        class="cursor-pointer px-2"
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
    column-gap: 3px;
  }

  .nav-right-container {
    display: flex;
    align-items: center;
    width: 70%;
    justify-content: space-between;

    & > span:first-child {
      flex-basis: 70%;
    }
  }
}
</style>
