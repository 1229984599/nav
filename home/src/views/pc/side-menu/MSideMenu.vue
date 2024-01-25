<script setup lang="ts">
import { useAppStore } from "@/store/app";
import MMenuItem from "./MMenuItem.vue";
import { useMenuStore } from "@/store/menu";
import { onMounted, ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { isMobile } from "@/utils/window";

const appStore = useAppStore();
const menuStore = useMenuStore();
const loading = ref(false);
onMounted(() => {
  loading.value = true;
  menuStore.getMenuTree().finally(() => (loading.value = false));
});
const target = ref(null);
onClickOutside(target, () => {
  if (isMobile.value) {
    appStore.isCollapse = true;
  }
});
</script>

<template>
  <el-menu
    v-loading.fullscreen.lock="loading"
    ref="target"
    :collapse-transition="false"
    :collapse="appStore.isCollapse"
    class="divide-y divide-gray-100"
  >
    <m-menu-item :item="item" v-for="item in menuStore.menuTree" />
  </el-menu>
</template>

<style scoped></style>
