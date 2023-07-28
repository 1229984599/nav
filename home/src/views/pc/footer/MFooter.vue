<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { scrollTop } from "@/utils/window";
import AddLink from "@/views/pc/footer/AddLink.vue";

defineOptions({
  name: "MFooter",
});
</script>

<template>
  <div>
    <!--友情链接-->
    <!--    <h2 class="text-zinc-900 font-black py-2">友情链接</h2>-->

    <div class="h-[70px] bg-white flex items-center">
      <ul class="flex px-2 gap-4 flex-wrap">
        <li><a href="#">链接一</a></li>
        <li><a href="#">链接二</a></li>
      </ul>
    </div>

    <footer class="mt-5">
      <!-- 版权信息 -->
      <div class="text-zinc-500">&copy;2017-2023 design by moxiaoying</div>
    </footer>
    <div
      class="right-4 fixed bottom-4 flex flex-col justify-center gap-y-3 cursor-pointer"
    >
      <!--      回到顶部-->
      <m-icon
        class="tool-item"
        @click="scrollTop('.el-main')"
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
