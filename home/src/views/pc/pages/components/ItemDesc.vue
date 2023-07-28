<script setup lang="ts">
import { PropType } from "vue";
import { ItemType } from "@/api/menu";

defineProps({
  item: Object as PropType<ItemType>,
});
</script>

<template>
  <a
    :href="item?.href"
    :target="item?.isSelf ? '_self' : '_blank'"
    class="cursor-pointer bg-white box rounded-lg p-4 flex space-x-2 items-center"
  >
    <div class="shrink-0">
      <img
        class="w-16 h-16 rounded-full"
        src="https://liutongxu.github.io/ico/gitee.png"
        :alt="item?.title"
      />
    </div>

    <div class="truncate">
      <div class="text-lg font-bold">{{ item.title }}</div>
      <span class="text-sm text-gray-600 w-full">
        {{ item?.desc ?? "暂无描述信息" }}
      </span>
    </div>
  </a>
</template>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}

.box {
  transition:
    box-shadow 0.3s,
    transform 0.3s,
    color 0.3s;
}

/* 鼠标放上去时的样式 */
.box:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加底部阴影 */
  transform: translateY(-2px); /* 向上移动一点的动画效果 */
  color: #cc2b2b;
}
</style>
