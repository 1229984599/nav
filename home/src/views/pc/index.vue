<script setup lang="ts">
import MSideMenu from "./side-menu/index.vue";
import MNavbar from "./navbar/index.vue";
import MLogo from "@/components/MLogo.vue";
import { useAppStore } from "@/store/app";
import MFooter from "./footer/index.vue";
import AppMain from "./app-main/AppMain.vue";
import { computed, onMounted } from "vue";
import { isMobile } from "@/utils/window";
import { useSiteStore } from "@/store/site";
import { useTitle } from "@vueuse/core";
import MSearch from "@/components/m-search/index.vue";
import MMask from "@/components/m-mask.vue";
import style from "@/styles/variables.module.scss";

const appStore = useAppStore();
const siteStore = useSiteStore();
onMounted(async () => {
  if (isMobile.value) {
    appStore.isCollapse = true;
  }
  await siteStore.getSiteInfo();
  useTitle(siteStore.siteInfo.title);
});
// 是否显示遮罩
const isMask = computed(() => {
  return isMobile.value ? !appStore.isCollapse : false;
});

// 左侧菜单宽带
const menuWidth = computed(() => {
  return appStore.isCollapse ? style.hideSideBarWidth : style.sideBarWidth;
});
</script>

<template>
  <div class="common-layout">
    <!--    左侧菜单-->
    <div class="left-container">
      <el-aside class="menu-side">
        <m-logo class="bg-white" />
        <m-side-menu />
      </el-aside>
    </div>
    <!--    右侧内容-->
    <div class="right-container">
      <m-navbar class="navbar" />
      <m-search />
      <div class="p-2 md:p-6">
        <app-main />
        <m-footer />
      </div>
    </div>
    <m-mask :is-mask="isMask" />
  </div>
</template>

<style scoped lang="scss">
@import "@/styles/variables.module";

.common-layout {
  display: flex;
  background-color: #{$bg};

  .left-container {
    height: 100vh;
    z-index: 60;

    ul {
      height: calc(100% - #{$navHeaderHeight});
      border-right: none;
    }

    .menu-side {
      position: relative;
      height: 100%;
      width: v-bind(menuWidth);
      transition: width #{$sideBarDuration} ease;
      @media screen and (max-width: 768px) {
        transition-duration: 0.25s;
      }
    }

    :deep(.el-menu--collapse) {
      width: 100%;
    }
  }

  .right-container {
    height: 100vh;
    width: 100%;
    overflow-y: auto;

    .navbar {
      height: #{$navHeaderHeight};
      width: 100%;
      position: sticky;
      top: 0;
      right: 0;
      z-index: 1;
      word-wrap: break-word;
      box-sizing: border-box;
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      transition:
        color 0.3s,
        background-color 0.3s;
      box-shadow: none;
      border-bottom-width: 1px;
      border-bottom-color: rgba(0, 0, 0, 0.06);
      background: rgba(255, 255, 255, 1);
    }
  }
}
</style>
