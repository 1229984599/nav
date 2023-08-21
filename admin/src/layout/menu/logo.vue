<script lang="ts">
export default {
  name: "MLogo",
};
</script>
<script setup lang="ts">
import MIcon from "@/components/icon.vue";
import { useAppStore } from "@/store";
const appStore = useAppStore();
const logoHeight = 44;
</script>

<template>
  <router-link
    key="collapse"
    class="logo-container px-5 decoration-none"
    :style="{ background: appStore.cssVar.menuBg }"
    to="/"
  >
    <m-icon icon="ion:logo-edge" color="white" :size="logoHeight" />
    <h1 class="logo-title" v-if="!appStore.isCollapse">哈哈后台管理</h1>
  </router-link>
</template>

<style lang="scss" scoped>
.logo-container {
  cursor: pointer;
  padding: 10px 0 10px 0;
  display: flex !important;
  align-items: center;
  justify-content: center;

  .logo-title {
    margin-left: 10px;
    color: #fff;
    font-weight: 600;
    line-height: 50px;
    font-size: 16px;
    white-space: nowrap;
  }
}
</style>
