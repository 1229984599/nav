<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, nextTick } from "vue";
import MIcon from "@/components/MIcon.vue";
import SearchSuggestionItem from "./SearchSuggestionItem.vue";
import { useSearch, useSearchActions } from "@/composables/useSearch";

defineOptions({
  name: "MSearchDialog",
});

const {
  engines,
  activeEngine,
  currentEngine,
  setEngine,
  fetchSuggestions,
} = useSearch();

const visible = ref(false);
const searchQuery = ref("");
const autocompleteRef = ref<any>(null);

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

const {
  removeHistoryAndRefresh,
  handleSuggestionClick,
  handleExternalSearch,
  handleEnterSearch,
} = useSearchActions(searchQuery, autocompleteRef, close);

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
      <div v-if="visible" class="search-overlay" role="dialog" aria-modal="true" aria-label="搜索" @click.self="close">
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
                  class="text-gray-400 dark:text-gray-500"
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
                <div class="flex items-center gap-x-2">
                  <m-icon
                    @click="handleExternalSearch(searchQuery)"
                    :icon="currentEngine.icon"
                    :size="20"
                    class="cursor-pointer text-gray-400 dark:text-gray-500 hover:text-blue-500 transition-colors"
                    :title="`用${currentEngine.label}搜索`"
                  />
                  <span
                    class="text-xs text-gray-400 dark:text-gray-500 border border-gray-300 dark:border-gray-600 rounded px-1.5 py-0.5 select-none"
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
