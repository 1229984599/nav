<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";

defineProps<{
  item: any;
  currentEngine: { key: string; label: string; icon: string; url: string };
}>();

defineEmits<{
  (e: "remove-history", keyword: string): void;
}>();
</script>

<template>
  <!-- History item -->
  <div v-if="item._isHistory" class="suggestion-item suggestion-history">
    <m-icon icon="mdi:history" :size="16" class="text-gray-400 dark:text-gray-500 flex-shrink-0" />
    <span class="suggestion-title">{{ item.title }}</span>
    <m-icon
      icon="mdi:close"
      :size="14"
      class="suggestion-remove"
      @mousedown.stop.prevent
      @click.stop.prevent="$emit('remove-history', item.title)"
    />
  </div>
  <!-- External suggestion -->
  <div v-else-if="item._isExternal" class="suggestion-item suggestion-external">
    <m-icon :icon="currentEngine.icon" :size="16" class="flex-shrink-0" />
    <span class="suggestion-title">{{ item.title }}</span>
    <span class="suggestion-badge external">{{ currentEngine.label }}</span>
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
      <span v-if="item.desc" class="suggestion-desc">{{ item.desc }}</span>
    </div>
    <span v-if="item.menus?.length" class="suggestion-badge menu">
      {{ item.menus[0].title }}
    </span>
  </div>
</template>

<style lang="scss" scoped>
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
    background: rgba(245, 158, 11, 0.15);
    color: #e5a00d;
  }
}
</style>
