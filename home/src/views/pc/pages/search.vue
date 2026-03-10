<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import linkModel from "@/api/links";
import { LinkSchemaList } from "@/api/links/types";
import MIcon from "@/components/MIcon.vue";
import EmptyState from "@/components/EmptyState.vue";
import SkeletonCard from "@/components/SkeletonCard.vue";

const route = useRoute();
const router = useRouter();

const keyword = computed(() => (route.query.q as string) || "");
const loading = ref(false);
const results = ref<LinkSchemaList[]>([]);

const HISTORY_KEY = "search-history";

function getHistory(): string[] {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
}

const searchHistory = ref<string[]>(getHistory());

function clearHistory() {
  localStorage.removeItem(HISTORY_KEY);
  searchHistory.value = [];
}

function removeHistoryItem(kw: string) {
  const history = getHistory().filter((h) => h !== kw);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  searchHistory.value = history;
}

function searchByHistory(kw: string) {
  router.push({ path: "/search", query: { q: kw } });
}

// Group by category
const groupedResults = computed(() => {
  const groups: Record<string, { menu: any; links: LinkSchemaList[] }> = {};
  for (const link of results.value) {
    const menuTitle = link.menus?.[0]?.title || "未分类";
    if (!groups[menuTitle]) {
      groups[menuTitle] = { menu: link.menus?.[0] || null, links: [] };
    }
    groups[menuTitle].links.push(link);
  }
  return groups;
});

const totalCount = computed(() => results.value.length);

// Highlight keyword
function highlightText(text: string): string {
  if (!keyword.value || !text) return text;
  const escaped = keyword.value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return text.replace(
    new RegExp(`(${escaped})`, "gi"),
    '<mark class="search-highlight">$1</mark>',
  );
}

// Sort by match priority: title > href > desc
function matchPriority(link: LinkSchemaList, q: string): number {
  const lower = q.toLowerCase();
  if (link.title?.toLowerCase().includes(lower)) return 0;
  if (link.href?.toLowerCase().includes(lower)) return 1;
  return 2;
}

async function doSearch(q: string) {
  if (!q.trim()) {
    results.value = [];
    return;
  }
  loading.value = true;
  try {
    const { items } = await linkModel.list(
      { page: 1, pageSize: 50, order_by: "order" },
      { keyword: q },
    );
    results.value = [...items].sort(
      (a, b) => matchPriority(a, q) - matchPriority(b, q),
    );
  } catch {
    results.value = [];
  } finally {
    loading.value = false;
  }
}

watch(keyword, (val) => doSearch(val), { immediate: true });
</script>

<template>
  <div class="search-page">
    <!-- Search header -->
    <div class="search-header" v-if="keyword">
      <div class="search-header-left">
        <m-icon icon="mingcute:search-line" :size="24" class="text-gray-400" />
        <h2 class="search-header-title">
          <span class="search-keyword">{{ keyword }}</span>
        </h2>
      </div>
      <span class="search-count" v-if="!loading">
        {{ totalCount }} 条结果
      </span>
    </div>

    <!-- No keyword: show history -->
    <div v-if="!keyword" class="search-empty-state">
      <div v-if="searchHistory.length > 0" class="history-section">
        <div class="history-header">
          <div class="history-header-left">
            <m-icon icon="mdi:history" :size="18" class="text-gray-400" />
            <h3>搜索历史</h3>
          </div>
          <button class="history-clear-btn" @click="clearHistory">
            <m-icon icon="mdi:delete-outline" :size="14" />
            清空
          </button>
        </div>
        <div class="history-tags">
          <div
            v-for="h in searchHistory"
            :key="h"
            class="history-tag"
            @click="searchByHistory(h)"
          >
            <span>{{ h }}</span>
            <m-icon
              icon="mdi:close"
              :size="12"
              class="history-tag-remove"
              @click.stop="removeHistoryItem(h)"
            />
          </div>
        </div>
      </div>
      <empty-state
        v-else
        icon="mingcute:search-line"
        text="输入关键词开始搜索"
      />
    </div>

    <!-- Loading skeleton -->
    <div
      v-else-if="loading"
      class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
    >
      <skeleton-card type="card" :count="8" />
    </div>

    <!-- No results -->
    <div v-else-if="results.length === 0" class="no-results">
      <empty-state icon="mdi:magnify-close" text="未找到匹配结果" />
      <p class="no-results-hint">试试搜索其他关键词，或检查拼写是否正确</p>
    </div>

    <!-- Results grouped by category -->
    <div v-else class="search-results">
      <div
        v-for="(group, menuTitle) in groupedResults"
        :key="menuTitle"
        class="result-group"
      >
        <div class="group-header">
          <div class="group-header-left">
            <m-icon
              v-if="group.menu?.icon"
              :icon="group.menu.icon"
              :color="group.menu.color"
              :size="18"
            />
            <h3>{{ menuTitle }}</h3>
          </div>
          <span class="group-count">{{ group.links.length }}</span>
        </div>
        <div
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 mb-6"
        >
          <a
            v-for="link in group.links"
            :key="link.id"
            :href="link.href"
            target="_blank"
            class="result-card"
          >
            <div class="result-card-icon">
              <m-icon
                :icon="link.icon || 'mdi:link-variant'"
                :color="link.color"
                :size="28"
              />
            </div>
            <div class="result-card-body">
              <span
                class="result-title"
                v-html="highlightText(link.title || '')"
              />
              <p
                class="result-desc"
                v-html="highlightText(link.desc || link.href || '')"
              />
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.search-page {
  padding-bottom: 32px;
}

.search-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: var(--nav-card-bg, #fff);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);

  @media screen and (max-width: 768px) {
    padding: 12px 14px;
    margin-bottom: 16px;
  }
}

.search-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.search-header-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-keyword {
  color: var(--el-color-primary, #409eff);
}

.search-count {
  flex-shrink: 0;
  font-size: 13px;
  color: var(--nav-text-secondary, #6b7280);
  padding: 2px 10px;
  background: var(--nav-bg, #f0f2f5);
  border-radius: 12px;
}

.search-empty-state {
  padding: 24px 0;
}

.history-section {
  max-width: 600px;
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.history-header-left {
  display: flex;
  align-items: center;
  gap: 6px;
  h3 {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
  }
}

.history-clear-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  font-size: 12px;
  color: var(--nav-text-secondary, #999);
  background: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;

  &:hover {
    background: rgba(239, 68, 68, 0.08);
    color: #ef4444;
  }
}

.history-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.history-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  font-size: 13px;
  color: var(--nav-text, #1f2937);
  background: var(--nav-card-bg, #fff);
  border: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;

  &:hover {
    border-color: var(--el-color-primary-light-5);
    color: var(--el-color-primary, #409eff);
    box-shadow: 0 2px 6px rgba(64, 158, 255, 0.1);
  }

  .history-tag-remove {
    opacity: 0;
    color: var(--nav-text-secondary, #999);
    transition: opacity 0.15s;
    &:hover {
      color: #ef4444;
    }
  }

  &:hover .history-tag-remove {
    opacity: 1;
  }
}

.no-results {
  text-align: center;
  padding: 40px 0;
}

.no-results-hint {
  margin-top: 8px;
  font-size: 13px;
  color: var(--nav-text-secondary, #999);
}

.group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.group-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  h3 {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
  }
}

.group-count {
  font-size: 12px;
  color: var(--nav-text-secondary, #999);
  padding: 1px 8px;
  background: var(--nav-bg, #f0f2f5);
  border-radius: 10px;
  line-height: 1.5;
}

.result-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: var(--space-3, 12px);
  background-color: var(--nav-card-bg);
  border-radius: 10px;
  border: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  text-decoration: none;
  color: inherit;
  transition:
    box-shadow 0.25s,
    border-color 0.25s,
    transform 0.15s;

  &:hover {
    border-color: var(--el-color-primary-light-5, rgba(64, 158, 255, 0.4));
    box-shadow:
      0 2px 4px rgba(0, 0, 0, 0.04),
      0 8px 16px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
    color: var(--el-color-primary);
  }

  &:active {
    transform: scale(0.98);
  }

  @media screen and (min-width: 769px) {
    padding: var(--space-4, 16px);
  }
}

.result-card-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: var(--nav-bg, #f0f2f5);
}

.result-card-body {
  flex: 1;
  overflow: hidden;
}

.result-title {
  display: block;
  font-size: 0.92rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-desc {
  margin-top: 3px;
  font-size: 0.75rem;
  color: var(--nav-text-secondary);
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  word-break: break-all;
}

:deep(.search-highlight) {
  background-color: rgba(64, 158, 255, 0.15);
  color: var(--el-color-primary);
  padding: 0 2px;
  border-radius: 2px;
}
</style>
