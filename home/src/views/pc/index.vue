<script setup lang="ts">
import MSideMenu from "./side-menu/index.vue";
import MNavbar from "./navbar/index.vue";
import MLogo from "@/components/MLogo.vue";
import { useAppStore } from "@/store/app";
import MFooter from "./footer/index.vue";
import AppMain from "./app-main/AppMain.vue";
import { computed, onMounted, provide, ref } from "vue";
import { isMobile } from "@/utils/window";
import { useSiteStore } from "@/store/site";
import { useBookmarkStore } from "@/store/bookmark";
import { useTitle } from "@vueuse/core";
import SearchDialog from "@/components/m-search/SearchDialog.vue";
import MMask from "@/components/m-mask.vue";
import style from "@/styles/variables.module.scss";
import { useScrollProgress } from "@/composables/useScrollProgress";

const appStore = useAppStore();
const siteStore = useSiteStore();
const bookmarkStore = useBookmarkStore();
const searchDialogRef = ref<InstanceType<typeof SearchDialog> | null>(null);

/** 从旧版 localMenu 格式迁移书签数据 */
function migrateOldBookmarks() {
  try {
    const raw = localStorage.getItem("menu");
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (parsed?.localMenu?.links?.length > 0 && bookmarkStore.links.length === 0) {
      bookmarkStore.migrateFromLegacy(parsed.localMenu.links);
    }
  } catch {
    // 迁移失败不影响正常使用
  }
}

function openSearch() {
  searchDialogRef.value?.open();
}

// Provide openSearch to child components (footer tool group)
provide("openSearch", openSearch);

onMounted(async () => {
  if (isMobile.value) {
    appStore.isCollapse = true;
  }
  migrateOldBookmarks();
  await siteStore.getSiteInfo();
  useTitle(siteStore.siteInfo.title);
});
// 是否显示遮罩
const isMask = computed(() => {
  return isMobile.value ? !appStore.isCollapse : false;
});

// 左侧菜单宽带
const menuWidth = computed(() => {
  if (!appStore.isCollapse) return style.sideBarWidth;
  return isMobile.value ? style.hideSideBarWidth : style.sidebarHideWidth;
});

// 滚动进度条
const { scrollProgress, scrollPercent } = useScrollProgress();

// Provide scrollProgress to child components (footer uses it)
provide("scrollProgress", scrollProgress);
</script>

<template>
  <div class="common-layout">
    <!--    左侧菜单-->
    <div class="left-container" role="navigation" aria-label="分类菜单">
      <el-aside class="menu-side">
        <m-logo :style="{ backgroundColor: 'var(--nav-logo-bg)' }" />
        <m-side-menu />
      </el-aside>
    </div>
    <!--    右侧内容-->
    <div class="right-container" role="main">
      <div class="scroll-progress" role="progressbar" :aria-valuenow="Math.round(scrollPercent)" aria-valuemin="0" aria-valuemax="100" :style="{ width: scrollPercent + '%' }" />
      <m-navbar class="navbar" @open-search="openSearch" />
      <div class="p-2 md:p-6">
        <app-main />
        <m-footer />
      </div>
    </div>
    <m-mask :is-mask="isMask" />

    <!-- 搜索对话框 -->
    <search-dialog ref="searchDialogRef" />
  </div>
</template>

<style scoped lang="scss">
@import "@/styles/variables.module";

.common-layout {
  display: flex;
  background-color: var(--nav-bg);

  .left-container {
    height: 100vh;
    z-index: 60;
    overflow: hidden;
    flex-shrink: 0;

    .menu-side {
      position: relative;
      display: flex;
      flex-direction: column;
      height: 100%;
      width: v-bind(menuWidth);
      min-width: v-bind(menuWidth);
      transition: width #{$sideBarDuration} cubic-bezier(0.25, 0.46, 0.45, 0.94),
                  min-width #{$sideBarDuration} cubic-bezier(0.25, 0.46, 0.45, 0.94);
      overflow: hidden;
      @media screen and (max-width: 768px) {
        transition-duration: 0.25s;
      }
    }

    :deep(.el-menu--collapse) {
      width: 100%;
    }
  }

  .right-container {
    height: 100vh;
    width: 100%;
    overflow-y: auto;

    .navbar {
      height: #{$navHeaderHeight};
      width: 100%;
      position: sticky;
      top: 0;
      right: 0;
      z-index: 1;
      word-wrap: break-word;
      box-sizing: border-box;
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      transition:
        color 0.3s,
        background-color 0.3s;
      box-shadow: none;
      border-bottom-width: 1px;
      border-bottom-color: var(--nav-border);
      background: var(--nav-navbar-bg);
    }
  }
}
</style>
