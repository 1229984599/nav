<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { scrollTop } from "@/utils/window";
import AddLink from "@/components/add-link/remote.vue";
import { useSiteStore } from "@/store/site";
import { useFriendStore } from "@/store/friend";
import { inject, onMounted, ref } from "vue";
import type { Ref } from "vue";
import SubMenuItem from "../side-menu/SubMenuItem.vue";
import { useUserStore } from "@/store/user";
import { useRouter } from "vue-router";
import EmptyState from "@/components/EmptyState.vue";

defineOptions({
  name: "MFooter",
});
const siteStore = useSiteStore();
const friendStore = useFriendStore();
const userStore = useUserStore();
const router = useRouter();
onMounted(friendStore.getFriendList);

const openSearch = inject<() => void>("openSearch", () => {});

// 滚动进度 (provided by parent pc/index.vue via useScrollProgress)
const scrollProgress = inject<Ref<number>>("scrollProgress", ref(0));

const item = {
  title: "友情链接",
  icon: "file-icons:freedos",
  color: "red",
};

function handleScrollTop() {
  router.push({
    name: "List",
    replace: true,
  });
  scrollTop(".right-container");
}
</script>

<template>
  <div>
    <!--友情链接-->
    <sub-menu-item :item="item" class="text-lg pb-2" :icon-size="32" />
    <div class="min-h-[70px] py-3 flex items-center" :style="{ backgroundColor: 'var(--nav-card-bg)' }">
      <ul v-if="friendStore.friendList.length > 0" class="flex px-2 gap-x-2 flex-wrap text-sm">
        <li class="list-disc mx-4" v-for="friend in friendStore.friendList">
          <a
            class="block max-w-[90px] text-sm whitespace-nowrap overflow-hidden text-ellipsis"
            :href="friend.href"
            target="_blank"
            :title="friend.title"
            >{{ friend.title }}</a
          >
        </li>
      </ul>
      <empty-state
        v-else
        icon="mdi:account-group-outline"
        text="暂无友情链接"
        :size="36"
        class="w-full"
      />
    </div>

    <footer class="mt-5" role="contentinfo">
      <!-- 版权信息 -->
      <span style="color: var(--nav-text-secondary)" class="text-sm">
        <a href="https://beian.miit.gov.cn" target="_blank">{{
          siteStore.siteInfo?.copyright
        }}</a>
      </span>
      <div
        style="color: var(--nav-text-secondary)"
        class="text-sm"
        v-text="siteStore.siteInfo?.footer"
      ></div>
    </footer>
    <div
      class="right-4 fixed bottom-4 flex flex-col justify-center gap-y-3 cursor-pointer"
      role="toolbar"
      aria-label="页面工具"
    >
      <el-tooltip content="搜索 (Ctrl+K)" placement="left">
        <button class="tool-item" aria-label="搜索" @click="openSearch">
          <m-icon icon="mingcute:search-line" />
        </button>
      </el-tooltip>
      <el-tooltip content="回到顶部" placement="left">
        <div class="back-top-wrapper" @click="handleScrollTop">
          <svg class="progress-ring" width="36" height="36" viewBox="0 0 36 36">
            <circle
              class="progress-ring-bg"
              cx="18" cy="18" r="15"
              fill="none"
              stroke="#e5e7eb"
              stroke-width="2"
            />
            <circle
              class="progress-ring-fill"
              cx="18" cy="18" r="15"
              fill="none"
              stroke="var(--el-color-primary, #409eff)"
              stroke-width="2"
              stroke-linecap="round"
              :stroke-dasharray="94.25"
              :stroke-dashoffset="94.25 * (1 - scrollProgress)"
              transform="rotate(-90 18 18)"
            />
          </svg>
          <m-icon
            class="back-top-icon"
            icon="ph:rocket-fill"
            :size="16"
          />
        </div>
      </el-tooltip>
      <el-tooltip content="mini书签" placement="left">
        <router-link :to="{ name: 'Mobile' }">
          <m-icon class="tool-item" icon="mingcute:wechat-miniprogram-fill" />
        </router-link>
      </el-tooltip>

      <!--      添加链接-->
      <add-link v-if="userStore.isAdminAuthorized" class="tool-item" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
a {
  text-decoration: none;
  color: inherit;
}

.tool-item {
  transition: color 0.35s ease;

  &:hover {
    color: var(--el-color-primary);
  }
}

.back-top-wrapper {
  position: relative;
  width: 36px;
  height: 36px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;

  .progress-ring {
    position: absolute;
    top: 0;
    left: 0;
  }

  .progress-ring-bg {
    opacity: 0.3;
  }

  .progress-ring-fill {
    transition: stroke-dashoffset 0.1s linear;
  }

  .back-top-icon {
    z-index: 1;
    color: var(--el-color-primary, #409eff);
    transition: color 0.2s;
  }

  &:hover .back-top-icon {
    color: #fe2d46;
  }
}
</style>
