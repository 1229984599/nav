<script setup lang="ts">
import { LocationQueryValue, useRoute } from "vue-router";
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";
import TabCategory from "./components/TabCategory.vue";
import { useTitle } from "@vueuse/core";
import { useSiteStore } from "@/store/site";
import BookmarkSection from "@/components/local-menu/BookmarkSection.vue";
import SkeletonCard from "@/components/SkeletonCard.vue";
import MIcon from "@/components/MIcon.vue";

const routes = useRoute();
const siteStore = useSiteStore();
const menuStore = useMenuStore();

function scrollToCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  if (!cat || typeof cat !== "string") return;
  nextTick(() => {
    const el = document.getElementById(cat);
    const container = document.querySelector(".right-container");
    if (el && container) {
      const containerHeight = container.clientHeight;
      const scrollTarget = el.offsetTop - containerHeight / 2 + 60;
      container.scroll({
        top: Math.max(0, scrollTarget),
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

// --- Intersection Observer: 滚动时自动高亮侧边栏 ---
const observer = ref<IntersectionObserver | null>(null);
const isUserScrolling = ref(true);

onMounted(() => {
  const container = document.querySelector(".right-container");
  if (!container) return;

  observer.value = new IntersectionObserver(
    (entries) => {
      if (!isUserScrolling.value) return;
      for (const entry of entries) {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.3) {
          const id = entry.target.id;
          if (id) {
            menuStore.setActiveMenuIndex(id);
          }
        }
      }
    },
    {
      root: container,
      rootMargin: "-80px 0px -60% 0px",
      threshold: 0.3,
    },
  );
});

// 菜单加载后，观察各分类区块
watch(
  () => menuStore.menuTree.length,
  (len) => {
    if (len > 0 && observer.value) {
      nextTick(() => {
        for (const item of menuStore.menuTree) {
          if (item.title) {
            const el = document.getElementById(item.title);
            if (el) observer.value!.observe(el);
          }
        }
      });
    }
  },
);

onBeforeUnmount(() => {
  observer.value?.disconnect();
});
</script>

<template>
  <div>
    <bookmark-section />

    <!-- 骨架屏：菜单数据加载中 -->
    <template v-if="menuStore.loading && menuStore.menuTree.length === 0">
      <div v-for="i in 2" :key="'sk-' + i" class="mb-8">
        <div class="flex items-center gap-x-2 mb-3">
          <div class="w-6 h-6 rounded bg-[#e9ecef] dark:bg-[#3a3a5a] skeleton-pulse" />
          <div class="w-24 h-6 rounded bg-[#e9ecef] dark:bg-[#3a3a5a] skeleton-pulse" />
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
          <skeleton-card type="card" :count="8" />
        </div>
      </div>
    </template>

    <!-- 加载失败：错误状态 + 重试 -->
    <div v-else-if="menuStore.loadError && menuStore.menuTree.length === 0" class="flex flex-col items-center justify-center py-20 gap-4">
      <m-icon icon="mdi:wifi-off" :size="48" style="color: var(--nav-text-secondary, #999)" />
      <p style="color: var(--nav-text-secondary, #6b7280)">菜单加载失败，请检查网络后重试</p>
      <button
        class="px-4 py-2 rounded-lg text-white text-sm"
        style="background: var(--el-color-primary, #409eff)"
        @click="menuStore.getMenuTree()"
      >
        重新加载
      </button>
    </div>

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
