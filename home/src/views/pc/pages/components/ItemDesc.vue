<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";

defineProps({
  item: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <a
    :href="item?.href"
    :target="item?.is_self ? '_self' : '_blank'"
    class="cursor-pointer bg-white box rounded-md p-4 flex space-x-2 items-center"
  >
    <div class="shrink-0">
      <m-icon
        :style="{ color: item?.color }"
        :icon="item.icon"
        :size="50"
        class="rounded-full"
      />
    </div>

    <div class="truncate pl-1.5">
      <div class="text-base font-bold">{{ item.title }}</div>
      <span class="desc">
        {{ item?.desc || "暂无描述信息" }}
      </span>
    </div>
  </a>
</template>

<style lang="scss" scoped>
.desc {
  @apply text-xs block h-[30px] mt-1 whitespace-normal text-gray-400 w-full duration-300 hover:text-gray-600;
  //text-indent: 10px;
}

img {
  @apply shadow;
}

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
