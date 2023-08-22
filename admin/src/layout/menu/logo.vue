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
  <a
    key="collapse"
    class="logo-container decoration-none py-2"
    :class="appStore.isCollapse ? 'justify-center' : 'pl-4'"
    :style="{ background: appStore.cssVar.menuBg }"
    href="/"
  >
    <m-icon icon="ion:logo-edge" color="white" :size="logoHeight" />
    <h1 class="logo-title" v-if="!appStore.isCollapse">哈哈导航</h1>
  </a>
</template>

<style lang="scss" scoped>
.logo-container {
  cursor: pointer;
  display: flex !important;
  align-items: center;
  //justify-content: center;

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
