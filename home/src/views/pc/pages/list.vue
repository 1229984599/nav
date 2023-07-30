<script setup lang="ts">
import { useRoute } from "vue-router";
import { watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";

const routes = useRoute();
const menuStore = useMenuStore();
watch(
  () => routes.query,
  (item) => {
    const el = document.querySelector(`#${item?.cat}`);
    if (el) {
      el.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  },
  {
    immediate: true,
  },
);
</script>

<template>
  <div v-for="menu in menuStore.menuTree">
    <item-category :menu="menu" />
    <div class="gap-y-6" v-if="menu?.children && menu.children.length > 0">
      <item-category :menu="subCat" v-for="subCat in menu.children" />
    </div>
  </div>
</template>

<style scoped></style>
