<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { scrollTop } from "@/utils/window";
import AddLink from "@/components/AddLink.vue";
import { useSiteStore } from "@/store/site";
import { useFriendStore } from "@/store/friend";
import { onMounted } from "vue";

defineOptions({
  name: "MFooter",
});
const siteStore = useSiteStore();
const friendStore = useFriendStore();
onMounted(friendStore.getFriendList);
</script>

<template>
  <div>
    <!--友情链接-->
    <!--    <h2 class="text-zinc-900 font-black py-2">友情链接</h2>-->

    <div class="h-[70px] bg-white flex items-center">
      <ul class="flex px-2 gap-4 flex-wrap text-sm">
        <li v-for="friend in friendStore.friendList">
          <a :href="friend.href" target="_blank">{{ friend.title }}</a>
        </li>
      </ul>
    </div>

    <footer class="mt-5">
      <!-- 版权信息 -->
      <div
        class="text-zinc-500 text-sm"
        v-html="siteStore.siteInfo?.footer"
      ></div>
    </footer>
    <div
      class="right-4 fixed bottom-4 flex flex-col justify-center gap-y-3 cursor-pointer"
    >
      <!--      回到顶部-->
      <m-icon
        class="tool-item"
        @click="scrollTop('.right-container')"
        icon="ph:rocket-fill"
      />
      <!--      添加链接-->
      <add-link class="tool-item" />
      <m-icon class="tool-item" icon="carbon:up-to-top" />
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
