<script setup lang="ts">
defineProps({
  item: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <el-tooltip
    effect="light"
    :content="item?.desc ?? '暂无描述信息'"
    placement="bottom"
  >
    <a
      :href="item?.href"
      :target="item?.isSelf ? '_self' : '_blank'"
      class="cursor-pointer bg-white box rounded-md p-4 flex space-x-2 items-center"
    >
      <div class="shrink-0">
        <img
          class="w-14 h-auto rounded-full"
          :src="item.icon"
          :alt="item?.title"
        />
      </div>

      <div class="truncate">
        <div class="text-lg font-bold">{{ item.title }}</div>
        <span class="desc">
          {{ item?.desc || "暂无描述信息" }}
        </span>
      </div>
    </a>
  </el-tooltip>
</template>

<style lang="scss" scoped>
.desc {
  @apply text-sm block h-[40px] mt-1 whitespace-normal text-gray-400 w-full duration-300 hover:text-gray-600;
  text-indent: 10px;
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
