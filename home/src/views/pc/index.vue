<script setup lang="ts">
import MSideMenu from "@/views/pc/side-menu/MSideMenu.vue";
import MNavbar from "@/views/pc/navbar/MNavbar.vue";
import MLogo from "@/components/MLogo.vue";
import { useAppStore } from "@/store/app";
import MFooter from "@/views/pc/footer/MFooter.vue";
import AppMain from "@/views/pc/app-main/AppMain.vue";
import { computed, onMounted } from "vue";
import { isMobile } from "@/utils/window";
import { useSiteStore } from "@/store/site";
import { useTitle } from "@vueuse/core";
import MSearch from "@/components/m-search/index.vue";
import MMask from "@/components/m-mask.vue";

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
</script>

<template>
  <div class="common-layout flex">
    <!--    左侧菜单-->
    <div class="h-screen left-container">
      <el-aside
        class="h-full relative"
        :class="appStore.isCollapse ? 'hide-menu-side' : 'menu-side'"
      >
        <m-logo class="bg-white" />
        <m-side-menu />
      </el-aside>
    </div>
    <!--    右侧内容-->
    <div class="h-screen right-container w-full overflow-y-auto">
      <m-navbar class="navbar border-b border-b-gray-100" />
      <m-search />
      <div class="p-2 md:p-6">
        <app-main />
        <m-footer />
      </div>
      <m-mask :is-mask="isMask" />
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.common-layout {
  background-color: #{$bg};

  .left-container {
    z-index: 60;
    ul {
      height: calc(100% - #{$navHeaderHeight});
      border-right: none;
    }

    .menu-side {
      width: #{$sideBarWidth};
      transition: width #{$sideBarDuration};
    }

    .hide-menu-side {
      width: #{$hideSideBarWidth};
      transition: width #{$sideBarDuration};
    }

    :deep(.el-menu--collapse) {
      width: 100%;
    }
  }

  .right-container {
    .navbar {
      height: 60px;
      width: 100%;
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      word-wrap: break-word;
      box-sizing: border-box;
      top: 0;
      z-index: 1;
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
</style>
