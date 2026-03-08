<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, nextTick } from "vue";
import linkModel from "@/api/links";
import MIcon from "@/components/MIcon.vue";
import { getBaiduSuggestions } from "@/api/spider";
import { useRouter } from "vue-router";

defineOptions({
  name: "MSearchDialog",
});

const router = useRouter();
const visible = ref(false);
const searchQuery = ref("");
const autocompleteRef = ref<any>(null);
const HISTORY_KEY = "search-history";
const MAX_HISTORY = 10;

function open() {
  visible.value = true;
  searchQuery.value = "";
  nextTick(() => {
    const inputEl = document.querySelector<HTMLInputElement>(
      ".search-dialog .el-input__inner",
    );
    inputEl?.focus();
  });
}

function close() {
  visible.value = false;
  searchQuery.value = "";
}

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
  close();
}

function handleBaiduSearch(kw: string = "") {
  if (kw === "") {
    window.open("https://www.baidu.com/s?wd=" + searchQuery.value, "_blank");
  } else if (typeof kw !== "object") {
    window.open("https://www.baidu.com/s?wd=" + kw, "_blank");
  }
  close();
}

// Enter 跳转搜索结果页
function handleEnterSearch() {
  if (!searchQuery.value.trim()) return;
  addHistory(searchQuery.value);
  router.push({ path: "/search", query: { q: searchQuery.value } });
  close();
}

// Ctrl+K / Cmd+K 全局快捷键
function handleGlobalKeydown(e: KeyboardEvent) {
  if ((e.ctrlKey || e.metaKey) && e.key === "k") {
    e.preventDefault();
    if (visible.value) {
      close();
    } else {
      open();
    }
  }
  if (e.key === "Escape" && visible.value) {
    close();
  }
}

onMounted(() => {
  document.addEventListener("keydown", handleGlobalKeydown);
});

onBeforeUnmount(() => {
  document.removeEventListener("keydown", handleGlobalKeydown);
});

defineExpose({ open, close });
</script>

<template>
  <teleport to="body">
    <transition name="search-fade">
      <div v-if="visible" class="search-overlay" @click.self="close">
        <div class="search-dialog">
          <div
            class="search-input-wrapper"
            @keydown.enter.prevent="handleEnterSearch"
          >
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
              class="w-full search-autocomplete"
              size="large"
              :popper-class="'search-dialog-popper'"
            >
              <template #prefix>
                <m-icon icon="mingcute:search-line" :size="20" class="text-gray-400" />
              </template>
              <template #default="{ item }">
                <div class="flex justify-between items-center py-1">
                  <div class="flex items-center gap-x-2 w-[70%]">
                    <m-icon
                      v-if="item.icon"
                      :icon="item.icon"
                      :color="item.color"
                      :size="20"
                      class="flex-shrink-0"
                    />
                    <span class="text-truncate">{{ item.title }}</span>
                  </div>
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
                      class="text-zinc-500 text-xs font-medium text-truncate"
                    >{{ item.menus[0].title }}</span>
                  </div>
                </div>
              </template>
              <template #suffix>
                <div class="flex items-center gap-x-2">
                  <m-icon
                    @click="handleBaiduSearch(searchQuery)"
                    icon="mingcute:search-line"
                    :size="22"
                    class="cursor-pointer text-gray-400 hover:text-blue-500 transition-colors"
                  />
                  <span
                    class="text-xs text-gray-400 border border-gray-300 rounded px-1.5 py-0.5 select-none"
                  >ESC</span>
                </div>
              </template>
            </el-autocomplete>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<style lang="scss" scoped>
.search-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 15vh;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
}

.search-dialog {
  width: 580px;
  max-width: 90vw;
  background: var(--nav-card-bg, #fff);
  border-radius: 12px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.search-input-wrapper {
  padding: 12px 16px;
}

.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

// 动画
.search-fade-enter-active {
  transition: opacity 0.2s ease;
  .search-dialog {
    transition: transform 0.2s ease, opacity 0.2s ease;
  }
}
.search-fade-leave-active {
  transition: opacity 0.15s ease;
  .search-dialog {
    transition: transform 0.15s ease, opacity 0.15s ease;
  }
}
.search-fade-enter-from {
  opacity: 0;
  .search-dialog {
    transform: scale(0.95) translateY(-10px);
    opacity: 0;
  }
}
.search-fade-leave-to {
  opacity: 0;
  .search-dialog {
    transform: scale(0.95) translateY(-10px);
    opacity: 0;
  }
}

:deep(.el-input__wrapper) {
  box-shadow: none !important;
  background: transparent;
  padding: 4px 8px;
}

:deep(.el-input__inner) {
  font-size: 16px;
}
</style>

<style lang="scss">
/* Global style: autocomplete popper must sit above the search overlay (z-index 9999) */
.search-dialog-popper {
  z-index: 10000 !important;
}
</style>
