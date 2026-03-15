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
  (e: "edit", link: LocalLink): void;
  (e: "delete", link: LocalLink): void;
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
    class="bookmark-grid"
    :class="mobile
      ? 'grid-cols-2 lg:grid-cols-3'
      : 'grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5'"
    :disabled="!isDraggable"
    :animation="200"
    ghost-class="drag-ghost"
    @end="emit('drag-end')"
  >
    <template v-for="link in links" :key="link.id">
      <div
        class="card-wrap"
        @contextmenu="emit('contextmenu', $event, link)"
        @touchstart.passive="mobile && emit('touchstart', $event, link)"
        @touchend.passive="emit('touchend')"
        @touchmove.passive="emit('touchmove')"
      >
        <a
          class="bk-card"
          :href="link.href"
          :target="link.is_self ? '_self' : '_blank'"
          @click="emit('click', link)"
        >
          <div class="card-accent" :style="{ backgroundColor: link.color || '#c0c4cc' }" />
          <div class="card-icon">
            <m-icon :icon="link.icon" :color="link.color" :size="38" />
          </div>
          <div class="card-body">
            <span class="card-title">{{ link.title }}</span>
            <p class="card-desc">{{ link.desc || link.href }}</p>
          </div>
          <span v-if="link.clickCount > 0" class="card-visits" :title="`访问 ${link.clickCount} 次`">
            {{ link.clickCount }}
          </span>
        </a>
        <div class="card-bar">
          <span class="bar-group" :title="getGroupNames(link.groupIds)">
            <m-icon icon="mdi:folder-outline" :size="12" />
            {{ getGroupNames(link.groupIds) }}
          </span>
          <div class="bar-actions">
            <span class="bar-btn" title="编辑" @click.stop.prevent="emit('edit', link)">
              <m-icon icon="mdi:pencil-outline" :size="14" />
            </span>
            <span class="bar-btn bar-btn-danger" title="删除" @click.stop.prevent="emit('delete', link)">
              <m-icon icon="mdi:trash-can-outline" :size="14" />
            </span>
          </div>
        </div>
      </div>
    </template>
  </VueDraggable>
</template>

<style lang="scss" scoped>
.drag-ghost { opacity: 0.4; }

.bookmark-grid {
  display: grid;
  gap: 14px;
}

.card-wrap {
  position: relative;
  border-radius: 10px;
  background-color: var(--nav-card-bg);
  overflow: hidden;
  transition: box-shadow 0.25s, transform 0.25s;

  &:hover {
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
    transform: translateY(-2px);
    .bar-actions { opacity: 1; }
    .card-accent { width: 5px; }
  }
}

.bk-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 14px 10px;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  position: relative;

  &:hover { color: var(--el-color-primary); }

  .card-accent {
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 0 4px 4px 0;
    transition: width 0.25s;
  }

  .card-icon { flex-shrink: 0; }

  .card-body {
    flex: 1;
    overflow: hidden;
    padding-left: 2px;
  }

  .card-title {
    display: block;
    font-size: 0.92rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .card-desc {
    margin: 3px 0 0;
    font-size: 0.72rem;
    color: var(--nav-text-secondary);
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    word-break: break-all;
    min-height: 28px;
    line-height: 1.3;
  }

  .card-visits {
    position: absolute;
    top: 8px; right: 10px;
    font-size: 10px;
    color: var(--nav-text-secondary);
    background: var(--el-fill-color-lighter);
    border-radius: 8px;
    padding: 1px 6px;
    line-height: 1.4;
  }
}

.card-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 28px;
  padding: 0 10px;
  border-top: 1px solid var(--nav-border);
  font-size: 11px;
  color: var(--nav-text-secondary);

  .bar-group {
    display: flex;
    align-items: center;
    gap: 3px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 120px;
  }

  .bar-actions {
    display: flex;
    gap: 2px;
    opacity: 0;
    transition: opacity 0.18s;
  }

  .bar-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px; height: 22px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.15s;
    color: var(--nav-text-secondary);

    &:hover {
      background: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
    }

    &.bar-btn-danger:hover {
      background: var(--el-color-danger-light-9);
      color: var(--el-color-danger);
    }
  }
}
</style>
