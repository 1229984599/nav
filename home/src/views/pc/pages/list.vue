<script setup lang="ts">
import { LocationQueryValue, useRoute } from "vue-router";
import { nextTick, watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";
import TabCategory from "./components/TabCategory.vue";
import { useTitle } from "@vueuse/core";
import { useSiteStore } from "@/store/site";
import BookmarkSection from "@/components/local-menu/BookmarkSection.vue";

const routes = useRoute();
const siteStore = useSiteStore();
const menuStore = useMenuStore();

function scrollToCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  if (!cat || typeof cat !== "string") return;
  nextTick(() => {
    const el = document.getElementById(cat);
    if (el) {
      document.querySelector(".right-container")?.scroll({
        top: el.offsetTop - 90,
        behavior: "smooth",
      });
    }
  });
}

// 根据 URL 中的 sub 参数激活对应的子分类 tab
function activateSubFromRoute() {
  const cat = routes.query?.cat;
  const sub = routes.query?.sub;
  if (!cat || !sub || typeof cat !== "string" || typeof sub !== "string") return;
  // 在 menuTree 中找到匹配的父分类和子分类
  const parent = menuStore.menuTree.find((m) => m.title === cat);
  if (!parent?.children) return;
  const child = parent.children.find((c) => c.title === sub);
  if (parent.id && child?.id) {
    menuStore.setActiveSubTab(parent.id, child.id);
  }
}

// 监听路由 query 变化（cat + sub + _t），处理滚动和 tab 切换
watch(
  () => ({ cat: routes.query?.cat, sub: routes.query?.sub, _t: routes.query?._t }),
  ({ cat }) => {
    const catStr = typeof cat === "string" ? cat : "";
    useTitle(`${siteStore.siteInfo.title} - ${catStr || "首页"}`);
    if (cat) {
      activateSubFromRoute();
      scrollToCategory(cat);
    }
  },
);

// 等待菜单数据加载完成后，处理初始 URL 定位（首次加载/刷新页面时）
watch(
  () => menuStore.menuTree.length,
  (len) => {
    if (len > 0 && routes.query?.cat) {
      activateSubFromRoute();
      scrollToCategory(routes.query.cat);
    }
  },
);
</script>

<template>
  <div>
    <bookmark-section />

    <div v-for="menuItem in menuStore.menuTree" :key="menuItem.id">
      <!-- 有子分类的菜单：使用 Tab 切换模式 -->
      <tab-category
        v-if="menuItem?.status && menuItem?.children && menuItem.children.length > 0"
        :menu="menuItem"
      />
      <!-- 无子分类的菜单：保持原有显示方式 -->
      <item-category
        v-else-if="menuItem?.status"
        :menu="menuItem"
      />
    </div>
  </div>
</template>
