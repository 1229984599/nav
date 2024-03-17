<script setup lang="ts">
import { LocationQueryValue, useRoute } from "vue-router";
import { onMounted, watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";
import { useTitle } from "@vueuse/core";
import { useSiteStore } from "@/store/site";
import MLocalMenu from "@/components/local-menu/index.vue";
import ItemDesc from "@/views/pc/pages/components/ItemDesc.vue";

const routes = useRoute();
const siteStore = useSiteStore();
const menuStore = useMenuStore();

function gotoCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  const el = document.querySelector(`#${cat}`);
  if (el) {
    document.querySelector(".right-container")?.scroll({
      top: el?.offsetTop - 90,
      behavior: "smooth",
    });
  }
}

watch(
  () => routes.query?.cat,
  (cat) => {
    useTitle(`${siteStore.siteInfo.title} - ${cat || "首页"}`);
    if (cat) {
      gotoCategory(cat);
    }
  },
);
onMounted(() => gotoCategory(routes.query?.cat));
</script>

<template>
  <m-local-menu #item-desc="{ item }">
    <item-desc :item="item" />
  </m-local-menu>
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
