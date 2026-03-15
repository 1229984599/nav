<script setup lang="ts">
import ItemDesc from "./ItemDesc.vue";
import MIcon from "@/components/MIcon.vue";
import { defineAsyncComponent, PropType, ref } from "vue";
import { MenuSchemaTree } from "@/api/menu/types";
const VueDraggable = defineAsyncComponent(() =>
  import("vue-draggable-plus").then((m) => m.VueDraggable)
);
import { isMobile } from "@/utils/window";
import LinkContextMenu from "@/components/link-context-menu/index.vue";
import EmptyState from "@/components/EmptyState.vue";
import { useLinkDrag } from "@/composables/useLinkDrag";
import { LinkSchemaList } from "@/api/links/types";

const props = defineProps({
  menu: {
    type: Object as PropType<MenuSchemaTree>,
  },
});

const {
  isAdmin,
  editMode,
  isDragActive,
  linkList,
  orderSaving,
  handleLinkDragStart,
  handleLinkDragEnd,
} = useLinkDrag(() => props.menu?.links);

const contextMenuRef = ref<InstanceType<typeof LinkContextMenu>>();

function handleItemContextMenu(event: MouseEvent, item: LinkSchemaList) {
  if (!isAdmin.value) return;
  contextMenuRef.value?.show(event, item);
}
</script>

<template>
  <div :id="menu?.title" class="flex gap-x-2 items-center">
    <m-icon
      v-if="menu?.icon"
      :style="{ color: menu?.color }"
      :icon="menu.icon"
    />
    <h2 class="text-xl font-bold">{{ menu?.title }}</h2>
    <button
      v-if="isAdmin && isMobile"
      class="edit-mode-btn"
      :class="{ active: editMode }"
      @click="editMode = !editMode"
    >
      <m-icon :icon="editMode ? 'mdi:check' : 'mdi:sort-variant'" :size="14" />
      {{ editMode ? '完成' : '排序' }}
    </button>
  </div>
  <VueDraggable
    v-if="isDragActive"
    v-model="linkList"
    :disabled="orderSaving"
    class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mb-8 mt-3"
    :animation="200"
    ghost-class="drag-ghost"
    @start="handleLinkDragStart"
    @end="handleLinkDragEnd"
  >
    <item-desc :item="item" v-for="item in linkList" :key="item.id" @contextmenu="handleItemContextMenu" />
  </VueDraggable>
  <div
    v-else
    class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mb-8 mt-3"
  >
    <item-desc :item="item" v-for="item in menu?.links" />
  </div>
  <empty-state
    v-if="(!menu?.links || menu.links.length === 0)"
    icon="mdi:link-off"
    text="该分类暂无链接"
    class="mb-8"
  />
  <link-context-menu v-if="isAdmin" ref="contextMenuRef" />
</template>

<style lang="scss" scoped>
.edit-mode-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 10px;
  font-size: 12px;
  line-height: 1.6;
  border-radius: 12px;
  border: 1px solid var(--el-border-color, #dcdfe6);
  background: var(--el-bg-color, #fff);
  color: var(--nav-text-secondary, #666);
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;

  &.active {
    color: #fff;
    background: var(--el-color-primary, #409eff);
    border-color: var(--el-color-primary, #409eff);
  }
}
</style>
