<script setup lang="ts">
import { ref } from "vue";
import MIcon from "@/components/MIcon.vue";
import MLogo from "@/components/MLogo.vue";
import SearchSuggestionItem from "./SearchSuggestionItem.vue";
import { useSearch, useSearchActions } from "@/composables/useSearch";

defineOptions({
  name: "MSearch",
});

const searchQuery = ref("");
const autocompleteRef = ref<any>(null);

const {
  engines,
  activeEngine,
  currentEngine,
  setEngine,
  fetchSuggestions,
} = useSearch();

const {
  removeHistoryAndRefresh,
  handleSuggestionClick,
  handleExternalSearch,
  handleEnterSearch,
} = useSearchActions(searchQuery, autocompleteRef, () => {
  searchQuery.value = "";
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
              class="text-gray-400 dark:text-gray-500 ml-1"
            />
          </template>
          <template #default="{ item }">
            <search-suggestion-item
              :item="item"
              :current-engine="currentEngine"
              @remove-history="removeHistoryAndRefresh"
            />
          </template>
          <template #suffix>
            <m-icon
              @click="handleExternalSearch(searchQuery)"
              :icon="currentEngine.icon"
              :size="22"
              class="cursor-pointer h-full text-gray-400 dark:text-gray-500 hover:text-blue-500 transition-colors"
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

.input-container {
  width: 100%;
  position: relative;
  box-shadow: rgba(64, 145, 247, 0.2) 0 0 3px;
  border-radius: 999px;
}

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

:deep(.el-autocomplete-suggestion__list > li) {
  border-bottom: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));

  &:last-child {
    border-bottom: none;
  }
}
</style>
