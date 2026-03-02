<script setup lang="ts">
import { LocationQueryValue, useRoute } from "vue-router";
import { onMounted, ref, watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";
import { useTitle } from "@vueuse/core";
import { useSiteStore } from "@/store/site";
import BookmarkSection from "@/components/local-menu/BookmarkSection.vue";
import { VueDraggable } from "vue-draggable-plus";
import { useUserStore } from "@/store/user";
import menu from "@/api/menu";

const routes = useRoute();
const siteStore = useSiteStore();
const menuStore = useMenuStore();
const userStore = useUserStore();

const isAdmin = ref(!!userStore.token?.access_token);

function gotoCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  if (!cat || typeof cat !== 'string') return;
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

async function handleMenuDragEnd() {
  const updates: Array<{ id: number; order: number }> = [];
  menuStore.menuTree.forEach((item, index) => {
    if (item.id) {
      updates.push({ id: item.id, order: index });
    }
  });
  if (updates.length === 0) return;
  try {
    await menu.batchUpdate(updates);
    await menuStore.getMenuTree();
  } catch (e) {
    console.error("菜单排序保存失败", e);
  }
}
</script>

<template>
  <div>
    <bookmark-section />

    <VueDraggable
      v-if="isAdmin"
      v-model="menuStore.menuTree"
      handle=".menu-drag-handle"
      :animation="150"
      @end="handleMenuDragEnd"
    >
      <div v-for="menuItem in menuStore.menuTree" :key="menuItem.id">
        <item-category :menu="menuItem" v-if="menuItem?.status" />
        <div
          class="gap-y-6"
          v-if="menuItem?.children && menuItem.children.length > 0 && menuItem?.status"
        >
          <item-category :menu="subCat" v-for="subCat in menuItem.children" :key="subCat.id" />
        </div>
      </div>
    </VueDraggable>

    <template v-else>
      <div v-for="menuItem in menuStore.menuTree">
        <item-category :menu="menuItem" v-if="menuItem?.status" />
        <div
          class="gap-y-6"
          v-if="menuItem?.children && menuItem.children.length > 0 && menuItem?.status"
        >
          <item-category :menu="subCat" v-for="subCat in menuItem.children" />
        </div>
      </div>
    </template>
  </div>
</template>
