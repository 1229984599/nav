<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { scrollTop } from "@/utils/window";
import AddLink from "@/components/AddLink.vue";
import { useSiteStore } from "@/store/site";
import { useFriendStore } from "@/store/friend";
import { onMounted } from "vue";
import SubMenuItem from "../side-menu/SubMenuItem.vue";
import { useUserStore } from "@/store/user";

defineOptions({
  name: "MFooter",
});
const siteStore = useSiteStore();
const friendStore = useFriendStore();
const userStore = useUserStore();
onMounted(friendStore.getFriendList);
const item = {
  title: "友情链接",
  icon: "file-icons:freedos",
  color: "red",
};

function handleScrollTop() {
  location.hash = "#/list";
  scrollTop(".right-container");
}
</script>

<template>
  <div>
    <!--友情链接-->
    <!--    <h2 class="text-zinc-900 font-black py-2">友情链接</h2>-->
    <sub-menu-item :item="item" class="text-lg pb-2" :icon-size="37" />
    <div class="h-[70px] bg-white flex items-center">
      <ul class="flex px-2 gap-4 flex-wrap text-sm">
        <li class="list-disc mx-4" v-for="friend in friendStore.friendList">
          <a
            class="block max-w-[120px] text-sm whitespace-nowrap overflow-clip"
            :href="friend.href"
            target="_blank"
            >{{ friend.title }}</a
          >
        </li>
      </ul>
    </div>

    <footer class="mt-5">
      <!-- 版权信息 -->
      <span class="text-zinc-500 text-sm">
        <a href="https://beian.miit.gov.cn" target="_blank">{{
          siteStore.siteInfo?.copyright
        }}</a>
      </span>
      <div
        class="text-zinc-500 text-sm"
        v-html="siteStore.siteInfo?.footer"
      ></div>
    </footer>
    <div
      class="right-4 fixed bottom-4 flex flex-col justify-center gap-y-3 cursor-pointer"
    >
      <m-icon
        class="tool-item"
        @click="handleScrollTop"
        icon="ph:rocket-fill"
      />
      <!--      添加链接-->
      <add-link v-if="userStore.token?.access_token" class="tool-item" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
a {
  text-decoration: none;
  color: inherit;
}

.tool-item {
  @apply hover:text-red-900;
}
</style>
