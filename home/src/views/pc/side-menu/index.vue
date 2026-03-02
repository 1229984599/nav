<script setup lang="ts">
import { useAppStore } from "@/store/app";
import MMenuItem from "./MMenuItem.vue";
import SubMenuItem from "./SubMenuItem.vue";
import { useMenuStore } from "@/store/menu";
import { useBookmarkStore } from "@/store/bookmark";
import { onMounted, ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { isMobile } from "@/utils/window";
import { useRouter } from "vue-router";
import MIcon from "@/components/MIcon.vue";

defineOptions({
  name: "MSideMenu",
});
const appStore = useAppStore();
const menuStore = useMenuStore();
const bookmarkStore = useBookmarkStore();
const router = useRouter();
const loading = ref(false);

onMounted(() => {
  loading.value = true;
  menuStore.getMenuTree().finally(() => (loading.value = false));
});

const targetRef = ref(null);
onClickOutside(targetRef, () => {
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
    document.querySelector(".right-container")?.scroll({
      top: el.offsetTop - 90,
      behavior: "smooth",
    });
  }
}
</script>

<template>
  <el-menu
    v-loading.fullscreen.lock="loading"
    ref="targetRef"
    :collapse-transition="false"
    :collapse="appStore.isCollapse"
    class="divide-y divide-gray-100"
  >
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
  </el-menu>
</template>

<style scoped></style>
