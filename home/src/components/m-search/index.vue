<script lang="ts">
export default {
  name: "MSearch",
};
</script>
<script setup lang="ts">
import { computed, onMounted, Ref, ref } from "vue";
import linkModel from "@/api/links";
import MIcon from "@/components/MIcon.vue";
import { useSiteStore } from "@/store/site";
import MLogo from "@/components/MLogo.vue";

defineOptions({
  name: "MSearch",
});
const siteStore = useSiteStore();
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
  callback(items);
}

// 搜索功能
function handleSuggestionClick(link: any) {
  window.open(link.href, "_blank");
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
          :highlight-first-item="true"
          :fit-input-width="true"
          :trigger-on-focus="true"
          value-key="title"
          v-model="searchQuery"
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

    <!--    搜索推荐-->
    <!-- 第四栏：通知 -->
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-input__wrapper) {
  border-color: transparent !important;
  box-shadow: none !important;
}

/* 去掉li标签前面的小圆点，鼠标放上去有一个小手出现 */
li {
  list-style: none;
  cursor: pointer;
  /* 导航栏高亮时在文字底部添加一个白色下划线 */
  span {
    transition: width 0.3s ease;
  }

  &:hover span {
    width: 100%;
  }
}

.nav-item {
  transition: color 0.5s;
  cursor: pointer;

  &:hover {
    @apply text-white;
  }
}

.nav-active {
  @apply text-white font-bold;
}

//.active {
//  &:after {
//    color: white;
//  }
//}
</style>
