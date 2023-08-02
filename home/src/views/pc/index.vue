<script setup lang="ts">
import MSideMenu from "@/views/pc/side-menu/MSideMenu.vue";
import MNavbar from "@/views/pc/navbar/MNavbar.vue";
import MLogo from "@/components/MLogo.vue";
import { useAppStore } from "@/store/app";
import MFooter from "@/views/pc/footer/MFooter.vue";
import AppMain from "@/views/pc/app-main/AppMain.vue";
import { onMounted } from "vue";
import { isMobile } from "@/utils/window";
import { useSiteStore } from "@/store/site";
import { useTitle } from "@vueuse/core";
import MSearch from "@/components/MSearch.vue";

const appStore = useAppStore();
const siteStore = useSiteStore();
onMounted(async () => {
  if (isMobile.value) {
    appStore.isCollapse = true;
  }
  await siteStore.getSiteInfo();
  useTitle(siteStore.siteInfo.title);
});
</script>

<template>
  <div class="common-layout flex">
    <!--    左侧菜单-->
    <div class="h-screen left-container">
      <el-aside
        class="h-full"
        :class="appStore.isCollapse ? 'hide-menu-side' : 'menu-side'"
      >
        <m-logo />
        <m-side-menu />
      </el-aside>
    </div>
    <!--    右侧内容-->
    <div
      class="h-screen right-container overflow-y-auto"
      :class="appStore.isCollapse ? 'hide-right-main' : 'right-main'"
    >
      <div class="nav-search">
        <m-navbar class="navbar" />
        <m-search class="py-40 flex justify-center" />
      </div>
      <div class="p-6">
        <app-main />
        <m-footer />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.common-layout {
  background-color: #{$bg};

  .nav-search {
    color: #282a2d;
    position: relative;
    background-size: 400%;
    background-position: 0% 100%;
    animation: gradient 7.5s ease-in-out infinite;
    background-image: linear-gradient(
      45deg,
      #8618db 0%,
      #d711ff 50%,
      #460fdd 100%
    );
    .navbar {
      height: 60px;
      width: 100%;
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      word-wrap: break-word;
      box-sizing: border-box;
      top: 0;
      z-index: 1080;
      position: sticky;
      right: 0;
      transition:
        color 0.3s,
        background-color 0.3s;
      box-shadow: none;
      color: initial;
      background: rgba(255, 255, 255, 1);
    }
  }
}

ul {
  height: calc(100% - #{$navHeaderHeight});
  border-right: none;
}

.menu-side {
  width: #{$sideBarWidth};
}

.hide-menu-side {
  width: #{$hideSideBarWidth};
}

.right-main {
  width: calc(100% - #{$sideBarWidth});
}

.hide-right-main {
  width: calc(100% - #{$hideSideBarWidth});
}
</style>
