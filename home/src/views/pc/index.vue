<script setup lang="ts">
import MSideMenu from "@/views/pc/side-menu/MSideMenu.vue";
import MNavbar from "@/views/pc/navbar/MNavbar.vue";
import MLogo from "@/components/MLogo.vue";
import { useAppStore } from "@/store/app";
import MFooter from "@/views/pc/footer/MFooter.vue";
import AppMain from "@/views/pc/app-main/AppMain.vue";
import { computed, onMounted } from "vue";
import { isMobile } from "@/utils/window";

const appStore = useAppStore();
onMounted(() => {
  if (isMobile.value) {
    appStore.isCollapse = true;
  }
});
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
