<script setup lang="ts">
import { LocationQueryValue, useRoute } from "vue-router";
import { onMounted, watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";

const routes = useRoute();
const menuStore = useMenuStore();

function gotoCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  const el = document.querySelector(`#${cat}`);
  if (el) {
    el.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
    // el.scrollTop = 60;
    // el.offsetTop += 50;
    // debugger;
  }
}
watch(
  () => routes.query,
  (item) => {
    gotoCategory(item?.cat);
  },
  {
    immediate: true,
  },
);
onMounted(() => {
  gotoCategory(routes.query?.cat);
});
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
