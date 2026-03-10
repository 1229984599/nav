<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, nextTick, computed } from "vue";
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

// Search engines
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

function clearHistory() {
  localStorage.removeItem(HISTORY_KEY);
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
  close();
}

function handleExternalSearch(kw: string = "") {
  const q = kw || searchQuery.value;
  if (!q) return;
  addHistory(q);
  window.open(currentEngine.value.url + encodeURIComponent(q), "_blank");
  close();
}

// Enter: go to search results page
function handleEnterSearch() {
  if (!searchQuery.value.trim()) return;
  addHistory(searchQuery.value);
  router.push({ path: "/search", query: { q: searchQuery.value } });
  close();
}

// Ctrl+K / Cmd+K
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
          <!-- Search input -->
          <div
            class="search-input-wrapper"
            @keydown.enter.prevent="handleEnterSearch"
          >
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
              class="w-full search-autocomplete"
              size="large"
              :popper-class="'search-dialog-popper'"
            >
              <template #prefix>
                <m-icon
                  icon="mingcute:search-line"
                  :size="20"
                  class="text-gray-400"
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
                <div class="flex items-center gap-x-2">
                  <m-icon
                    @click="handleExternalSearch(searchQuery)"
                    :icon="currentEngine.icon"
                    :size="20"
                    class="cursor-pointer text-gray-400 hover:text-blue-500 transition-colors"
                    :title="`用${currentEngine.label}搜索`"
                  />
                  <span
                    class="text-xs text-gray-400 border border-gray-300 rounded px-1.5 py-0.5 select-none"
                  >ESC</span>
                </div>
              </template>
            </el-autocomplete>
          </div>

          <!-- Search engine selector + tips -->
          <div class="search-footer">
            <div class="engine-group">
              <button
                v-for="eng in engines"
                :key="eng.key"
                :class="[
                  'engine-btn',
                  { active: activeEngine === eng.key },
                ]"
                @click="setEngine(eng.key)"
                :title="eng.label"
              >
                <m-icon :icon="eng.icon" :size="14" />
                <span>{{ eng.label }}</span>
              </button>
            </div>
            <div class="search-tips">
              <span class="tip-key">Enter</span>
              <span>搜索</span>
              <span class="tip-key">Tab</span>
              <span>选择</span>
            </div>
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
  padding-top: 12vh;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(6px);

  @media screen and (max-width: 768px) {
    padding-top: 6vh;
  }
}

.search-dialog {
  width: 600px;
  max-width: 92vw;
  background: var(--nav-card-bg, #fff);
  border-radius: 16px;
  box-shadow:
    0 25px 60px -12px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.search-input-wrapper {
  padding: 16px 20px 8px;

  @media screen and (max-width: 768px) {
    padding: 12px 14px 6px;
  }
}

// Footer: engine selector + tips
.search-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 20px 12px;
  border-top: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));

  @media screen and (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 8px 14px 12px;
  }
}

.engine-group {
  display: flex;
  gap: 4px;
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

.search-tips {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--nav-text-secondary, #999);
}

.tip-key {
  display: inline-block;
  padding: 1px 6px;
  font-size: 11px;
  font-family: monospace;
  background: var(--nav-bg, #f0f2f5);
  border: 1px solid var(--nav-border, rgba(0, 0, 0, 0.08));
  border-radius: 4px;
  line-height: 1.5;
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

// Animation
.search-fade-enter-active {
  transition: opacity 0.2s ease;
  .search-dialog {
    transition:
      transform 0.2s ease,
      opacity 0.2s ease;
  }
}
.search-fade-leave-active {
  transition: opacity 0.15s ease;
  .search-dialog {
    transition:
      transform 0.15s ease,
      opacity 0.15s ease;
  }
}
.search-fade-enter-from {
  opacity: 0;
  .search-dialog {
    transform: scale(0.96) translateY(-8px);
    opacity: 0;
  }
}
.search-fade-leave-to {
  opacity: 0;
  .search-dialog {
    transform: scale(0.96) translateY(-8px);
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
/* Global: autocomplete popper above search overlay */
.search-dialog-popper {
  z-index: 10000 !important;

  .el-autocomplete-suggestion__list > li {
    border-bottom: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));

    &:last-child {
      border-bottom: none;
    }
  }
}
</style>
