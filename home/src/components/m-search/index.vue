<script lang="ts">
export default {
  name: "MSearch",
};
</script>
<script setup lang="ts">
import { ref } from "vue";
import linkModel from "@/api/links";
import MIcon from "@/components/MIcon.vue";
import MLogo from "@/components/MLogo.vue";
import { getBaiduSuggestions } from "@/api/spider";

defineOptions({
  name: "MSearch",
});
const searchQuery = ref("");

async function fetchSuggestions(
  queryString: string,
  callback: (arg: any) => void,
) {
  // 模拟根据搜索词过滤结果
  const { items } = await linkModel.list(
    { page: 1, pageSize: 10, order_by: "order" },
    { title: queryString },
  );
  // 如果items长度为0，就调用百度搜索数据
  if (items.length === 0) {
    const baiduSuggestions = await getBaiduSuggestions(queryString);
    return callback(baiduSuggestions);
  }
  callback(items);
}

// 搜索功能
function handleSuggestionClick(link: any) {
  // 没有提供链接就跳转到百度搜索
  if (!link.href) {
    handleBaiduSearch(link.title);
    return;
  }
  window.open(link.href, "_blank");
  searchQuery.value = "";
}

// 跳转到百度搜索
function handleBaiduSearch(kw: string = "") {
  if (kw === "") {
    window.open("https://www.baidu.com/s?wd=" + searchQuery.value, "_blank");
  } else if (typeof kw !== "object") {
    window.open("https://www.baidu.com/s?wd=" + kw, "_blank");
  }
  searchQuery.value = "";
}
</script>

<template>
  <div class="mx-auto pt-8 pb-4 relative">
    <m-logo font-size="22px" class="flex justify-center text-2xl" />

    <!-- 第二栏：搜索框 -->
    <div
      class="flex justify-center py-3"
      @keydown.enter="handleSuggestionClick"
    >
      <div class="relative w-4/5 md:w-1/2">
        <el-autocomplete
          autofocus
          :highlight-first-item="true"
          :fit-input-width="true"
          :trigger-on-focus="false"
          v-model="searchQuery"
          :fetch-suggestions="fetchSuggestions"
          @select="handleSuggestionClick"
          placeholder="请输入需要搜索的内容"
          class="w-full px-2 py-2 bg-white rounded-full"
        >
          <template #default="{ item }">
            <div class="flex justify-between">
              <span class="px-2 w-[70%] text-truncate">{{ item.title }}</span>
              <div class="flex items-center gap-x-1 overflow-hidden">
                <m-icon
                  :icon="item.menus[0].icon"
                  :color="item.menus[0].color"
                  :size="16"
                />
                <span
                  class="text-zinc-600 min-w-[4em] text-sm font-bold text-truncate"
                  >{{ item.menus[0].title }}</span
                >
              </div>
            </div>
          </template>
          <template #suffix>
            <m-icon
              @click="handleBaiduSearch(searchQuery)"
              icon="mingcute:search-line"
              :size="28"
              class="cursor-pointer h-full"
            />
          </template>
        </el-autocomplete>
      </div>
    </div>

    <!--    搜索推荐-->
    <!-- 第四栏：通知 -->
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-input__wrapper) {
  border-color: transparent;
  box-shadow: none;
}

.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
