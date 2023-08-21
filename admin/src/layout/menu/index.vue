<script lang="ts">
export default {
  name: "MMenu",
};
</script>
<script setup lang="ts">
import { computed } from "vue";
import MSidebarMenu from "./sidebar-menu.vue";
import { useAppStore } from "@/store";
import { useRoute } from "vue-router";
import MLogo from "./logo.vue";

const route = useRoute();
const activeName = computed(() => {
  return route.path;
});
const appStore = useAppStore();
</script>

<template>
  <div class="h-full">
    <m-logo />
    <el-menu
      :unique-opened="true"
      :default-active="activeName"
      :collapse="appStore.isCollapse"
      :background-color="appStore.cssVar.menuBg"
      :active-text-color="appStore.cssVar.menuActiveText"
      :text-color="appStore.cssVar.menuText"
      :router="true"
    >
      <m-sidebar-menu />
    </el-menu>
  </div>
</template>

<style lang="scss" scoped>
.el-menu {
  border: none;

  :deep(.is-active) {
    background: #4091f7;
  }
}
</style>
