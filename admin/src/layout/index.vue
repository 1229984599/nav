<script setup lang="ts">
import MSidebar from "./menu/index.vue";
import MAppMain from "./main/index.vue";
import MHeader from "./header/index.vue";
import variables from "@/styles/variables.module.scss";
import { useAppStore } from "@/store";

const appStore = useAppStore();
</script>

<template>
  <div
    class="app-wrapper"
    :class="appStore.isCollapse ? 'hideSidebar' : 'openSidebar'"
  >
    <!-- 左侧 menu -->
    <m-sidebar
      id="guide-sidebar"
      :style="{ backgroundColor: variables.menuBg }"
      class="sidebar-container"
    />
    <div class="main-container">
      <div class="fixed-header">
        <!-- 顶部的 navbar -->
        <m-header />
      </div>
      <!-- 内容区 -->
      <m-app-main />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/styles/mixin.scss";
@import "@/styles/variables.module.scss";

.app-wrapper {
  @include clearfix;
  display: flex;
  height: 100%;
  width: 100%;
}

.fixed-header {
  width: 100%;
  height: #{$headerHeight};
}
</style>
