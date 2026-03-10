<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from "vue";
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

// Search engines (shared with SearchDialog)
const engines = [
  { key: "baidu", label: "百度", icon: "simple-icons:baidu", url: "https://www.baidu.com/s?wd=" },
  { key: "google", label: "Google", icon: "logos:google-icon", url: "https://www.google.com/search?q=" },
  { key: "bing", label: "Bing", icon: "logos:bing", url: "https://www.bing.com/search?q=" },
  { key: "github", label: "GitHub", icon: "mdi:github", url: "https://github.com/search?q=" },
];
const ENGINE_STORAGE_KEY = "search-engine";
const activeEngine = ref(localStorage.getItem(ENGINE_STORAGE_KEY) || "baidu");
const currentEngine = computed(() => engines.find((e) => e.key === activeEngine.value) || engines[0]);

function setEngine(key: string) {
  activeEngine.value = key;
  localStorage.setItem(ENGINE_STORAGE_KEY, key);
}

// Search history
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

function removeHistory(keyword: string) {
  const history = getHistory().filter((h) => h !== keyword);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

function removeHistoryAndRefresh(keyword: string) {
  removeHistory(keyword);
  // Close and reopen to refresh the suggestion list
  autocompleteRef.value?.close();
  nextTick(() => {
    autocompleteRef.value?.focus();
  });
}

// Sort by match priority: title > href > desc
function sortByMatchPriority(items: any[], q: string) {
  const lower = q.toLowerCase();
  return [...items].sort((a, b) => {
    const pa = a.title?.toLowerCase().includes(lower) ? 0
      : a.href?.toLowerCase().includes(lower) ? 1 : 2;
    const pb = b.title?.toLowerCase().includes(lower) ? 0
      : b.href?.toLowerCase().includes(lower) ? 1 : 2;
    return pa - pb;
  });
}

async function fetchSuggestions(
  queryString: string,
  callback: (arg: any) => void,
) {
  if (!queryString.trim()) {
    // Show history when empty
    const history = getHistory();
    if (history.length) {
      return callback(
        history.map((h) => ({ title: h, _isHistory: true })),
      );
    }
    return callback([]);
  }
  const { items } = await linkModel.list(
    { page: 1, pageSize: 8, order_by: "order" },
    { keyword: queryString },
  );
  if (items.length === 0) {
    const baiduSuggestions = await getBaiduSuggestions(queryString);
    return callback(
      baiduSuggestions.map((s: any) => ({ ...s, _isExternal: true })),
    );
  }
  callback(sortByMatchPriority(items, queryString));
}

function handleSuggestionClick(link: any) {
  if (link._isHistory) {
    searchQuery.value = link.title;
    handleEnterSearch();
    return;
  }
  if (!link.href) {
    handleExternalSearch(link.title);
    return;
  }
  addHistory(searchQuery.value || link.title);
  window.open(link.href, "_blank");
  searchQuery.value = "";
}

function handleExternalSearch(kw: string = "") {
  const q = kw || searchQuery.value;
  if (!q) return;
  addHistory(q);
  window.open(currentEngine.value.url + encodeURIComponent(q), "_blank");
  searchQuery.value = "";
}

// Enter: go to search results page
function handleEnterSearch() {
  if (!searchQuery.value.trim()) return;
  addHistory(searchQuery.value);
  router.push({ path: "/search", query: { q: searchQuery.value } });
}

// Ctrl+K / Cmd+K
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

    <!-- Search input -->
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
          :trigger-on-focus="true"
          :debounce="300"
          v-model="searchQuery"
          :fetch-suggestions="fetchSuggestions"
          @select="handleSuggestionClick"
          placeholder="搜索链接、描述、网址..."
          class="w-full px-2 py-2 rounded-full m-search-input"
          :style="{ backgroundColor: 'var(--nav-card-bg)' }"
        >
          <template #prefix>
            <m-icon
              icon="mingcute:search-line"
              :size="20"
              class="text-gray-400 ml-1"
            />
          </template>
          <template #default="{ item }">
            <!-- History item -->
            <div
              v-if="item._isHistory"
              class="suggestion-item suggestion-history"
            >
              <m-icon
                icon="mdi:history"
                :size="16"
                class="text-gray-400 flex-shrink-0"
              />
              <span class="suggestion-title">{{ item.title }}</span>
              <m-icon
                icon="mdi:close"
                :size="14"
                class="suggestion-remove"
                @mousedown.stop.prevent
                @click.stop.prevent="removeHistoryAndRefresh(item.title)"
              />
            </div>
            <!-- External suggestion -->
            <div
              v-else-if="item._isExternal"
              class="suggestion-item suggestion-external"
            >
              <m-icon
                :icon="currentEngine.icon"
                :size="16"
                class="flex-shrink-0"
              />
              <span class="suggestion-title">{{ item.title }}</span>
              <span class="suggestion-badge external">{{
                currentEngine.label
              }}</span>
            </div>
            <!-- Normal link result -->
            <div v-else class="suggestion-item">
              <m-icon
                v-if="item.icon"
                :icon="item.icon"
                :color="item.color"
                :size="20"
                class="flex-shrink-0"
              />
              <div class="suggestion-body">
                <span class="suggestion-title">{{ item.title }}</span>
                <span v-if="item.desc" class="suggestion-desc">{{
                  item.desc
                }}</span>
              </div>
              <span
                v-if="item.menus?.length"
                class="suggestion-badge menu"
              >
                {{ item.menus[0].title }}
              </span>
            </div>
          </template>
          <template #suffix>
            <m-icon
              @click="handleExternalSearch(searchQuery)"
              :icon="currentEngine.icon"
              :size="22"
              class="cursor-pointer h-full text-gray-400 hover:text-blue-500 transition-colors"
              :title="`用${currentEngine.label}搜索`"
            />
          </template>
        </el-autocomplete>
      </div>
    </div>

    <!-- Engine selector row -->
    <div class="engine-row">
      <button
        v-for="eng in engines"
        :key="eng.key"
        :class="['engine-btn', { active: activeEngine === eng.key }]"
        @click="setEngine(eng.key)"
      >
        <m-icon :icon="eng.icon" :size="14" />
        <span>{{ eng.label }}</span>
      </button>
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

// Engine selector row
.engine-row {
  display: flex;
  justify-content: center;
  gap: 6px;
  padding: 0 12px;
}

.engine-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  font-size: 12px;
  color: var(--nav-text-secondary, #6b7280);
  background: transparent;
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;

  &:hover {
    background: var(--el-color-primary-light-9, rgba(64, 158, 255, 0.08));
    color: var(--el-color-primary, #409eff);
  }

  &.active {
    background: var(--el-color-primary-light-9, rgba(64, 158, 255, 0.1));
    color: var(--el-color-primary, #409eff);
    border-color: var(--el-color-primary-light-7, rgba(64, 158, 255, 0.25));
    font-weight: 500;
  }
}

// Suggestion items
.suggestion-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 4px;
  min-height: 36px;
}

.suggestion-history {
  .suggestion-title {
    color: var(--nav-text-secondary, #6b7280);
  }

  .suggestion-remove {
    margin-left: auto;
    opacity: 0;
    cursor: pointer;
    color: var(--nav-text-secondary, #999);
    transition: opacity 0.15s;

    &:hover {
      color: #ef4444;
    }
  }

  &:hover .suggestion-remove {
    opacity: 1;
  }
}

.suggestion-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.suggestion-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
}

.suggestion-desc {
  font-size: 12px;
  color: var(--nav-text-secondary, #999);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.suggestion-badge {
  flex-shrink: 0;
  margin-left: auto;
  font-size: 11px;
  padding: 1px 8px;
  border-radius: 4px;
  line-height: 1.5;

  &.menu {
    background: var(--el-color-primary-light-9, rgba(64, 158, 255, 0.1));
    color: var(--el-color-primary, #409eff);
  }

  &.external {
    background: rgba(245, 158, 11, 0.1);
    color: #d97706;
  }
}

// Autocomplete suggestion item separators
:deep(.el-autocomplete-suggestion__list > li) {
  border-bottom: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));

  &:last-child {
    border-bottom: none;
  }
}
</style>
