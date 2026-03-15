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
  getGroupName: (id: string) => string;
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
    class="bookmark-list"
    :disabled="!isDraggable"
    :animation="200"
    ghost-class="drag-ghost"
    @end="emit('drag-end')"
  >
    <template v-for="link in links" :key="link.id">
      <div
        class="list-row"
        @contextmenu="emit('contextmenu', $event, link)"
        @touchstart.passive="mobile && emit('touchstart', $event, link)"
        @touchend.passive="emit('touchend')"
        @touchmove.passive="emit('touchmove')"
      >
        <a
          class="list-link"
          :href="link.href"
          :target="link.is_self ? '_self' : '_blank'"
          @click="emit('click', link)"
        >
          <m-icon :icon="link.icon" :color="link.color" :size="24" class="flex-shrink-0" />
          <span class="list-title">{{ link.title }}</span>
          <template v-for="gid in link.groupIds" :key="gid">
            <span class="list-group-tag">{{ getGroupName(gid) }}</span>
          </template>
          <span class="list-url">{{ link.href }}</span>
        </a>
        <div class="list-meta">
          <span v-if="link.clickCount > 0" class="list-visits">{{ link.clickCount }} 次</span>
          <span class="list-action" title="编辑" @click.stop="emit('edit', link)">
            <m-icon icon="mdi:pencil-outline" :size="15" />
          </span>
          <span class="list-action list-action-danger" title="删除" @click.stop="emit('delete', link)">
            <m-icon icon="mdi:trash-can-outline" :size="15" />
          </span>
        </div>
      </div>
    </template>
  </VueDraggable>
</template>

<style lang="scss" scoped>
.drag-ghost { opacity: 0.4; }

.bookmark-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.list-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.15s;

  &:hover {
    background-color: var(--nav-card-bg);
    .list-action { opacity: 1; }
  }
}

.list-link {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
  text-decoration: none;
  color: inherit;
  cursor: pointer;

  &:hover { color: var(--el-color-primary); }

  .list-title {
    font-size: 0.88rem;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 220px;
  }

  .list-group-tag {
    font-size: 11px;
    color: var(--el-color-primary);
    background: var(--el-color-primary-light-9);
    border-radius: 4px;
    padding: 1px 6px;
    white-space: nowrap;
    flex-shrink: 0;
    line-height: 1.4;
  }

  .list-url {
    font-size: 0.72rem;
    color: var(--nav-text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
  }
}

.list-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  margin-left: 8px;

  .list-visits {
    font-size: 0.72rem;
    color: var(--nav-text-secondary);
  }

  .list-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px; height: 24px;
    border-radius: 4px;
    cursor: pointer;
    opacity: 0;
    transition: all 0.15s;
    color: var(--nav-text-secondary);

    &:hover {
      background: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
    }

    &.list-action-danger:hover {
      background: var(--el-color-danger-light-9);
      color: var(--el-color-danger);
    }
  }
}
</style>
