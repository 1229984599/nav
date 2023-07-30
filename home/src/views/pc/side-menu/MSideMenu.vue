<script setup lang="ts">
import { useAppStore } from "@/store/app";
import MMenuItem from "./MMenuItem.vue";
import { useMenuStore } from "@/store/menu";
import { onMounted } from "vue";

const appStore = useAppStore();
const menuStore = useMenuStore();
onMounted(() => {
  menuStore.getMenuTree();
  menuStore.getMenuList();
});
</script>

<template>
  <el-menu
    :collapse-transition="false"
    :collapse="appStore.isCollapse"
    class="divide-y divide-gray-100"
  >
    <m-menu-item :item="item" v-for="item in menuStore.menuTree" />
  </el-menu>
</template>

<style scoped></style>
