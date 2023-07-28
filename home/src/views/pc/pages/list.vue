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
  <div v-for="category in menuStore.menuList">
    <item-category :category="category" />
    <div
      class="gap-y-6"
      v-if="category?.children && category.children.length > 0"
    >
      <item-category :category="subCat" v-for="subCat in category.children" />
    </div>
  </div>
</template>

<style scoped></style>
