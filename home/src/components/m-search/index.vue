<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import linkModel from "@/api/links";
import MIcon from "@/components/MIcon.vue";
import MLogo from "@/components/MLogo.vue";
import { getBaiduSuggestions } from "@/api/spider";
import { useRouter } from "vue-router";

defineOptions({
  name: "MSearch",
});

const router = useRouter();
const searchQuery = ref("");
const autocompleteRef = ref<any>(null);
const HISTORY_KEY = "search-history";
const MAX_HISTORY = 10;

// 搜索历史
function getHistory(): string[] {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
}

function addHistory(keyword: string) {
  if (!keyword.trim()) return;
  const history = getHistory().filter((h) => h !== keyword);
  history.unshift(keyword);
  localStorage.setItem(
    HISTORY_KEY,
    JSON.stringify(history.slice(0, MAX_HISTORY)),
  );
}

async function fetchSuggestions(
  queryString: string,
  callback: (arg: any) => void,
) {
  const { items } = await linkModel.list(
    { page: 1, pageSize: 10, order_by: "order" },
    { title: queryString },
  );
  if (items.length === 0) {
    const baiduSuggestions = await getBaiduSuggestions(queryString);
    return callback(baiduSuggestions);
  }
  callback(items);
}

function handleSuggestionClick(link: any) {
  if (!link.href) {
    handleBaiduSearch(link.title);
    return;
  }
  addHistory(searchQuery.value || link.title);
  window.open(link.href, "_blank");
  searchQuery.value = "";
}

function handleBaiduSearch(kw: string = "") {
  if (kw === "") {
    window.open("https://www.baidu.com/s?wd=" + searchQuery.value, "_blank");
  } else if (typeof kw !== "object") {
    window.open("https://www.baidu.com/s?wd=" + kw, "_blank");
  }
  searchQuery.value = "";
}

// Enter 跳转搜索结果页
function handleEnterSearch() {
  if (!searchQuery.value.trim()) return;
  addHistory(searchQuery.value);
  router.push({ path: "/search", query: { q: searchQuery.value } });
}

// Ctrl+K / Cmd+K 全局快捷键
function handleGlobalKeydown(e: KeyboardEvent) {
  if ((e.ctrlKey || e.metaKey) && e.key === "k") {
    e.preventDefault();
    const inputEl = document.querySelector<HTMLInputElement>(
      ".m-search-input .el-input__inner",
    );
    inputEl?.focus();
  }
}

onMounted(() => {
  document.addEventListener("keydown", handleGlobalKeydown);
});

onBeforeUnmount(() => {
  document.removeEventListener("keydown", handleGlobalKeydown);
});
</script>

<template>
  <div class="mx-auto pt-8 pb-4 relative">
    <m-logo v-bind="$attrs" class="flex justify-center text-2xl" />

    <!-- 搜索框 -->
    <div
      class="flex justify-center py-3"
      @keydown.enter.prevent="handleEnterSearch"
    >
      <div class="input-container">
        <el-autocomplete
          ref="autocompleteRef"
          autofocus
          :highlight-first-item="true"
          :fit-input-width="true"
          :trigger-on-focus="false"
          :debounce="300"
          v-model="searchQuery"
          :fetch-suggestions="fetchSuggestions"
          @select="handleSuggestionClick"
          placeholder="搜索链接... (Ctrl+K)"
          class="w-full px-2 py-2 rounded-full m-search-input"
          :style="{ backgroundColor: 'var(--nav-card-bg)' }"
        >
          <template #default="{ item }">
            <div class="flex justify-between">
              <span class="px-2 w-[70%] text-truncate">{{ item.title }}</span>
              <div
                class="flex items-center gap-x-1 overflow-hidden"
                v-if="item.menus?.length"
              >
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
.input-container {
  width: 100%;
  position: relative;
  box-shadow: rgba(64, 145, 247, 0.2) 0 0 3px;
  border-radius: 999px;
}
</style>
