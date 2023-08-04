<script lang="ts">
export default {
  name: "MSearch",
};
</script>
<script setup lang="ts">
import { computed, onMounted, Ref, ref } from "vue";
import MNotify from "./notify.vue";
import { useSearchStore } from "@/store/search";
import linkModel from "@/api/links";
import MIcon from "@/components/MIcon.vue";

defineOptions({
  name: "MSearch",
});

const searchStore = useSearchStore();

const searchQuery = ref("");

async function fetchSuggestions(
  queryString: string,
  callback: (arg: any) => void,
) {
  // 模拟根据搜索词过滤结果
  const { items } = await linkModel.list(1, 10, { title: queryString });
  callback(items);
}

// 搜索功能
function handleSuggestionClick(link: any) {
  // 在这里处理搜索逻辑，你可以根据searchQuery的值来进行搜索
  // console.log("搜索内容：", currentSearchUrl.value);
  // window.open(currentSearchUrl.value, "_blank");
  window.open(link.href, "_blank");
  searchQuery.value = "";
}

const currentSearchUrl = computed(() => {
  return `${searchStore.currentItem.href}${searchQuery.value}`;
});

onMounted(searchStore.initCurrentItem);
</script>

<template>
  <div class="mx-auto py-20 relative">
    <!-- 第一栏：导航分类 -->
    <nav class="flex justify-center">
      <ul class="flex space-x-6">
        <li
          v-for="category in searchStore.categoryList"
          :key="category.id"
          @click="searchStore.changeCurrentCategory(category.id)"
          :class="{
            'nav-active': searchStore.currentCategory.id === category.id,
          }"
          class="nav-item"
        >
          {{ category.title }}
          <span
            v-if="searchStore.currentCategory.id === category.id"
            class="block h-1 bg-white w-2/3 mx-auto mt-1 rounded-full"
          ></span>
        </li>
      </ul>
    </nav>

    <!-- 第二栏：搜索框 -->
    <div
      class="flex justify-center py-3"
      @keydown.enter="handleSuggestionClick"
    >
      <div class="relative w-4/5 md:w-1/2">
        <el-autocomplete
          :trigger-on-focus="false"
          :highlight-first-item="true"
          :fit-input-width="true"
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
        <div
          class="cursor-pointer absolute top-1 right-0 h-full py-1"
          @click="handleSuggestionClick"
        >
          <div class="ic:outline-search w-8 h-8 text-white"></div>
        </div>
      </div>
    </div>

    <!-- 第三栏：子导航 -->
    <nav class="flex justify-center">
      <ul class="flex space-x-6 h-4">
        <li
          v-for="(item, index) in searchStore.currentCategory.children"
          :key="index"
          @click="searchStore.changeCurrentItem(item.title)"
          class="opacity-100"
        >
          {{ item.title }}
        </li>
        <li style="display: none">dsfsd</li>
      </ul>
    </nav>
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
