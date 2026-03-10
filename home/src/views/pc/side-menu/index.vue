<script setup lang="ts">
import { useAppStore } from "@/store/app";
import MMenuItem from "./MMenuItem.vue";
import SubMenuItem from "./SubMenuItem.vue";
import { useMenuStore } from "@/store/menu";
import { useBookmarkStore } from "@/store/bookmark";
import { onMounted, nextTick, ref, watch } from "vue";
import { onClickOutside } from "@vueuse/core";
import { isMobile } from "@/utils/window";
import { useRouter } from "vue-router";
import MIcon from "@/components/MIcon.vue";
import SkeletonCard from "@/components/SkeletonCard.vue";

defineOptions({
  name: "MSideMenu",
});
const appStore = useAppStore();
const menuStore = useMenuStore();
const bookmarkStore = useBookmarkStore();
const router = useRouter();
const loading = ref(false);
const menuRef = ref<any>(null);

onMounted(() => {
  loading.value = true;
  menuStore.getMenuTree().finally(() => (loading.value = false));
});

// 监听 activeMenuIndex 变化，主动展开对应父菜单并高亮子项，滚动到可视区域
watch(
  () => menuStore.activeMenuIndex,
  (index) => {
    if (!index || !menuRef.value) return;
    // 移动端侧边栏已收起，不展开子菜单（避免弹出侧边栏）
    if (isMobile.value && appStore.isCollapse) return;
    // 找到子项对应的父菜单，展开它
    for (const item of menuStore.menuTree) {
      if (item.children && item.children.length > 0) {
        const matched = item.children.find((c) => c.title === index);
        if (matched && item.title) {
          menuRef.value.open(item.title);
          break;
        }
      }
    }
    // 等待 DOM 更新后，将高亮菜单项滚动到可视区域
    nextTick(() => {
      const menuEl = menuRef.value?.$el as HTMLElement | undefined;
      if (!menuEl) return;
      const activeItem = menuEl.querySelector(".el-menu-item.is-active") as HTMLElement | null;
      if (activeItem) {
        activeItem.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }
    });
  },
);

onClickOutside(menuRef, () => {
  if (isMobile.value) {
    appStore.isCollapse = true;
  }
});

function scrollToBookmarks(groupId?: string) {
  if (groupId) {
    bookmarkStore.setActiveGroup(groupId);
  } else {
    bookmarkStore.setActiveGroup(null);
  }
  router.push({ path: "/list", query: { cat: "本地书签" }, replace: true });
  const el = document.getElementById("本地书签");
  if (el) {
    const container = document.querySelector(".right-container");
    if (container) {
      const containerHeight = container.clientHeight;
      const scrollTarget = el.offsetTop - containerHeight / 2 + 60;
      container.scroll({
        top: Math.max(0, scrollTarget),
        behavior: "smooth",
      });
    }
  }
}
</script>

<template>
  <el-menu
    ref="menuRef"
    :default-active="menuStore.activeMenuIndex"
    :collapse-transition="false"
    :collapse="appStore.isCollapse"
    unique-opened
    class="divide-y divide-gray-100"
  >
    <!-- 加载骨架 -->
    <template v-if="loading">
      <skeleton-card type="menu" :count="6" />
    </template>
    <template v-else>
    <!-- 书签分组 -->
    <el-sub-menu index="local-bookmarks">
      <template #title>
        <div @click="scrollToBookmarks()" class="flex items-center">
          <sub-menu-item
            :item="{ title: '本地书签', icon: 'ion:bookmarks', color: '#C71585' }"
          />
        </div>
      </template>
      <el-menu-item
        v-for="group in bookmarkStore.sortedGroups"
        :key="group.id"
        :index="'bk-' + group.id"
        @click="scrollToBookmarks(group.id)"
      >
        <div class="flex items-center justify-between w-full">
          <div class="flex items-center">
            <m-icon :icon="group.icon" :color="group.color" :size="18" class="pr-1" />
            <span class="text-sm">{{ group.name }}</span>
          </div>
          <span class="text-xs text-gray-400 ml-1">{{ bookmarkStore.groupCounts[group.id] || 0 }}</span>
        </div>
      </el-menu-item>
    </el-sub-menu>

    <!-- 服务端菜单 -->
    <m-menu-item :item="item" v-for="item in menuStore.menuTree" />
    </template>
  </el-menu>
</template>

<style scoped>
:deep(.el-menu-item.is-active) {
  background-color: var(--el-color-primary-light-9, rgba(64, 158, 255, 0.1));
  border-radius: 6px;
  margin: 0 6px;
  width: calc(100% - 12px);
}
</style>
