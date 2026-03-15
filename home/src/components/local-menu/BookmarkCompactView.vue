<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import MIcon from "@/components/MIcon.vue";
import type { LocalLink } from "@/types/bookmark";

const VueDraggable = defineAsyncComponent(() =>
  import("vue-draggable-plus").then((m) => m.VueDraggable)
);

defineProps<{
  links: LocalLink[];
  allLinks: LocalLink[];
  isDraggable: boolean;
  mobile?: boolean;
  getGroupNames: (ids: string[]) => string;
}>();

const emit = defineEmits<{
  (e: "update:allLinks", value: LocalLink[]): void;
  (e: "click", link: LocalLink): void;
  (e: "contextmenu", event: MouseEvent | TouchEvent, link: LocalLink): void;
  (e: "drag-end"): void;
  (e: "touchstart", event: TouchEvent, link: LocalLink): void;
  (e: "touchend"): void;
  (e: "touchmove"): void;
}>();
</script>

<template>
  <VueDraggable
    :model-value="allLinks"
    @update:model-value="$emit('update:allLinks', $event)"
    class="bookmark-compact"
    :class="mobile
      ? 'grid-cols-4 lg:grid-cols-5 xl:grid-cols-6'
      : 'grid-cols-5 lg:grid-cols-7 xl:grid-cols-9 2xl:grid-cols-11'"
    :disabled="!isDraggable"
    :animation="200"
    ghost-class="drag-ghost"
    @end="emit('drag-end')"
  >
    <template v-for="link in links" :key="link.id">
      <a
        class="compact-item"
        :href="link.href"
        :target="link.is_self ? '_self' : '_blank'"
        @click="emit('click', link)"
        @contextmenu="emit('contextmenu', $event, link)"
        @touchstart.passive="mobile && emit('touchstart', $event, link)"
        @touchend.passive="emit('touchend')"
        @touchmove.passive="emit('touchmove')"
      >
        <div class="compact-icon">
          <m-icon :icon="link.icon" :color="link.color" :size="32" />
        </div>
        <span class="compact-title">{{ link.title }}</span>
        <span class="compact-group">{{ getGroupNames(link.groupIds) }}</span>
      </a>
    </template>
  </VueDraggable>
</template>

<style lang="scss" scoped>
.drag-ghost { opacity: 0.4; }

.bookmark-compact {
  display: grid;
  gap: 8px 6px;
}

.compact-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  padding: 10px 6px 8px;
  border-radius: 10px;
  transition: all 0.2s;

  &:hover {
    background-color: var(--nav-card-bg);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transform: translateY(-1px);
  }

  .compact-icon {
    width: 44px; height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: var(--el-fill-color-lighter);
    transition: background 0.2s;
  }

  &:hover .compact-icon {
    background: var(--el-color-primary-light-9);
  }

  .compact-title {
    font-size: 12px;
    max-width: 72px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: center;
  }

  .compact-group {
    font-size: 10px;
    color: var(--nav-text-secondary);
    max-width: 72px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: center;
    line-height: 1;
  }
}
</style>
