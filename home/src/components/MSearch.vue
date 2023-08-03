<script setup lang="ts">
import { ref } from "vue";
import MIcon from "@/components/MIcon.vue";
import linkModel from "@/api/links";
import { LinkSchemaList } from "@/api/links/types";

const searchValue = ref("");

const fetchSuggestions = async (
  queryString: string,
  callback: (arg: any) => void,
) => {
  // 模拟根据搜索词过滤结果
  const { items } = await linkModel.list(1, 10, { title: queryString });
  callback(items);
};

const handleSuggestionClick = (link: LinkSchemaList) => {
  // 点击搜索推荐结果，处理相应的操作
  window.open(link.href, "_blank");
  searchValue.value = "";
};
</script>

<template>
  <div class="mx-auto pb-20 pt-10 relative">
    <div class="w-3/5">
      <ul
        class="pb-3 flex justify-center gap-x-10 cursor-pointer text-gray-200/50"
      >
        <li class="li-item">百度</li>
        <li class="li-item">百度</li>
        <li class="li-item">百度</li>
      </ul>
      <el-autocomplete
        :trigger-on-focus="false"
        :highlight-first-item="true"
        :fit-input-width="true"
        value-key="title"
        v-model="searchValue"
        :fetch-suggestions="fetchSuggestions"
        @select="handleSuggestionClick"
        placeholder="请输入需要搜索的站点"
        class="w-full px-2 py-2 bg-white rounded-full"
      >
        <template #suffix>
          <m-icon
            icon="mingcute:search-line"
            size="28"
            class="cursor-pointer h-full"
          />
        </template>
      </el-autocomplete>
    </div>
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-input__wrapper) {
  border-color: transparent !important;
  box-shadow: none !important;
}

.li-item {
  border-bottom-width: 3px;
  word-break: keep-all;
  border-bottom-color: rgba(255, 255, 255, 0.01);
  transition: color 0.3s ease-in-out;
  &:hover,
  &:active {
    color: rgb(255 255 255);
    border-bottom-color: rgb(255 255 255);
  }
}
</style>
