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
        block: "center",
      });
      // el.scrollTop = 60;
      // el.offsetTop += 50;
      // debugger;
    }
  },
  {
    immediate: true,
  },
);
</script>

<template>
  <div v-for="menu in menuStore.menuTree">
    <!--    菜单启用-->
    <item-category :menu="menu" v-if="menu?.status" />
    <!--    有子类并且菜单启用-->
    <div
      class="gap-y-6"
      v-if="menu?.children && menu.children.length > 0 && menu?.status"
    >
      <item-category :menu="subCat" v-for="subCat in menu.children" />
    </div>
  </div>
</template>

<style scoped></style>
