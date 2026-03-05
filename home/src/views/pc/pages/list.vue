<script setup lang="ts">
import { LocationQueryValue, useRoute } from "vue-router";
import { onMounted, watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";
import { useTitle } from "@vueuse/core";
import { useSiteStore } from "@/store/site";
import BookmarkSection from "@/components/local-menu/BookmarkSection.vue";

const routes = useRoute();
const siteStore = useSiteStore();
const menuStore = useMenuStore();

function gotoCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  if (!cat || typeof cat !== "string") return;
  const el = document.getElementById(cat);
  if (el) {
    document.querySelector(".right-container")?.scroll({
      top: el.offsetTop - 90,
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
  <div>
    <bookmark-section />

    <div v-for="menuItem in menuStore.menuTree" :key="menuItem.id">
      <item-category :menu="menuItem" v-if="menuItem?.status" />
      <div
        class="gap-y-6"
        v-if="menuItem?.children && menuItem.children.length > 0 && menuItem?.status"
      >
        <item-category :menu="subCat" v-for="subCat in menuItem.children" :key="subCat.id" />
      </div>
    </div>
  </div>
</template>
