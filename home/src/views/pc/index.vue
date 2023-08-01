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

const appStore = useAppStore();
const siteStore = useSiteStore();
onMounted(async () => {
  if (isMobile.value) {
    appStore.isCollapse = true;
  }
  await siteStore.getSiteInfo();
});

useTitle(siteStore.siteInfo.title);
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-aside :class="appStore.isCollapse ? 'hide-menu-side' : 'menu-side'">
        <m-logo />
        <m-side-menu />
      </el-aside>
      <el-container
        :class="appStore.isCollapse ? 'hide-right-main' : 'right-main'"
      >
        <el-header class="border-b-2 shadow-gray-200">
          <m-navbar />
        </el-header>
        <el-main>
          <app-main />
          <m-footer />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.common-layout {
  background-color: #{$bg};
}

:deep(.el-container) {
  height: 100vh;
}

ul {
  height: calc(100% - #{$navHeaderHeight});
  border-right: none;
}

.el-header {
  padding: 0;
  background-color: #{$bg};
  border-bottom: 1px solid #e8e8e8;
}

.menu-side {
  width: #{$sideBarWidth};
}

.hide-menu-side {
  width: #{$hideSideBarWidth};
}

.right-main {
  width: calc(100% - #{$sideBarWidth});
  transition: width 0.5s;
}

.hide-right-main {
  width: calc(100% - #{$hideSideBarWidth});
  transition: width 0.5s;
}
</style>
