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
};
</script>

<template>
  <div class="container mx-auto py-10">
    <div class="relative w-3/5">
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

<style lang="scss">
.el-input__wrapper {
  border-color: transparent !important;
  box-shadow: none !important;
}
</style>
