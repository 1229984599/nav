<script setup lang="ts">
import { useAppStore } from "@/store/app";
import MMenuItem from "./MMenuItem.vue";
import { useMenuStore } from "@/store/menu";
import { onMounted, ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { isMobile } from "@/utils/window";

const appStore = useAppStore();
const menuStore = useMenuStore();
onMounted(() => {
  menuStore.getMenuTree();
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
    ref="target"
    :collapse-transition="false"
    :collapse="appStore.isCollapse"
    class="divide-y divide-gray-100"
  >
    <m-menu-item :item="item" v-for="item in menuStore.menuTree" />
  </el-menu>
</template>

<style scoped></style>
