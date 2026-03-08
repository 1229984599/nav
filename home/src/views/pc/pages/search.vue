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
const MAX_HISTORY = 10;

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

function searchByHistory(kw: string) {
  router.push({ path: "/search", query: { q: kw } });
}

// 按分类分组
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

// 高亮关键词
function highlightText(text: string): string {
  if (!keyword.value || !text) return text;
  const escaped = keyword.value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return text.replace(
    new RegExp(`(${escaped})`, "gi"),
    '<mark class="search-highlight">$1</mark>',
  );
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
      { title: q },
    );
    results.value = items;
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
    <!-- 搜索标题 -->
    <div class="search-header" v-if="keyword">
      <h2 class="text-xl font-bold">
        搜索结果：
        <span class="text-[var(--el-color-primary)]">{{ keyword }}</span>
      </h2>
      <span class="text-sm text-[var(--nav-text-secondary)]">
        {{ loading ? "搜索中..." : `共 ${results.length} 条结果` }}
      </span>
    </div>

    <!-- 无关键词：显示搜索历史 -->
    <div v-if="!keyword" class="search-history">
      <div v-if="searchHistory.length > 0" class="history-section">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-base font-bold">搜索历史</h3>
          <el-button size="small" text @click="clearHistory">
            <m-icon icon="mdi:delete-outline" :size="14" class="mr-1" />清空
          </el-button>
        </div>
        <div class="flex flex-wrap gap-2">
          <el-tag
            v-for="h in searchHistory"
            :key="h"
            class="cursor-pointer"
            @click="searchByHistory(h)"
          >
            {{ h }}
          </el-tag>
        </div>
      </div>
      <empty-state
        v-else
        icon="mdi:magnify"
        text="输入关键词开始搜索"
      />
    </div>

    <!-- 加载骨架 -->
    <div v-else-if="loading" class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <skeleton-card type="card" :count="8" />
    </div>

    <!-- 无结果 -->
    <empty-state
      v-else-if="results.length === 0"
      icon="mdi:magnify-close"
      text="未找到匹配结果"
    />

    <!-- 分组展示结果 -->
    <div v-else class="search-results">
      <div v-for="(group, menuTitle) in groupedResults" :key="menuTitle" class="result-group">
        <div class="flex items-center gap-x-2 mb-3">
          <m-icon
            v-if="group.menu?.icon"
            :icon="group.menu.icon"
            :color="group.menu.color"
            :size="20"
          />
          <h3 class="text-base font-bold">{{ menuTitle }}</h3>
          <span class="text-xs text-[var(--nav-text-secondary)]">{{ group.links.length }} 条</span>
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-6">
          <a
            v-for="link in group.links"
            :key="link.id"
            :href="link.href"
            target="_blank"
            class="result-card"
          >
            <div class="flex-shrink-0">
              <m-icon :icon="link.icon" :color="link.color" :size="32" class="rounded-full" />
            </div>
            <div class="result-card-body">
              <span class="result-title" v-html="highlightText(link.title || '')" />
              <p class="result-desc" v-html="highlightText(link.desc || link.href || '')" />
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
  align-items: baseline;
  gap: 12px;
  margin-bottom: 24px;
}

.search-history {
  padding: 24px 0;
}

.result-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: var(--space-3, 12px);
  background-color: var(--nav-card-bg);
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.3s, transform 0.15s;

  &:hover {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04), 0 8px 16px rgba(0, 0, 0, 0.08);
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
  margin-top: 4px;
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
