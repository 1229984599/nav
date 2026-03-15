<script setup lang="ts">
import { computed, ref } from "vue";
import { ElMessage } from "element-plus";
import MIcon from "@/components/MIcon.vue";
import MLocalAddLink from "@/components/add-link/local.vue";
import BookmarkGroupDialog from "./BookmarkGroupDialog.vue";
import BookmarkGridView from "./BookmarkGridView.vue";
import BookmarkCompactView from "./BookmarkCompactView.vue";
import BookmarkListView from "./BookmarkListView.vue";
import { useBookmarkStore } from "@/store/bookmark";
import { DEFAULT_GROUP_ID } from "@/types/bookmark";
import type { LocalLink, BookmarkGroup } from "@/types/bookmark";
import { useBookmarkContextMenu } from "./composables/useBookmarkContextMenu";
import { useBookmarkIO } from "./composables/useBookmarkIO";

defineOptions({ name: "BookmarkSection" });

const props = withDefaults(defineProps<{ mobile?: boolean }>(), { mobile: false });

const bookmarkStore = useBookmarkStore();
const linkDialogVisible = ref(false);
const linkRef = ref<InstanceType<typeof MLocalAddLink>>();
const groupDialogRef = ref<InstanceType<typeof BookmarkGroupDialog>>();
const groupDialogVisible = ref(false);

// ---- Computed ----

const displayLinks = computed(() => bookmarkStore.activeLinks);
const isDraggable = computed(() => bookmarkStore.sortMode === "manual");

// ---- Link Actions ----

function handleAddLink() {
  linkRef.value?.formRef?.value?.resetFields();
  linkRef.value?.setEditData({
    groupIds: bookmarkStore.activeGroupId ? [bookmarkStore.activeGroupId] : [DEFAULT_GROUP_ID],
  });
  linkDialogVisible.value = true;
}

function handleEditLink(link: LocalLink) {
  linkRef.value?.setEditData(link);
  linkDialogVisible.value = true;
}

function handleDeleteLink(link: LocalLink) {
  bookmarkStore.deleteLink(link.id);
  ElMessage.success("删除成功");
}

function handleLinkClick(link: LocalLink) {
  bookmarkStore.recordClick(link.id);
}

// ---- Group Actions ----

function handleAddGroup() {
  groupDialogRef.value?.open();
  groupDialogVisible.value = true;
}

function handleEditGroup(group: BookmarkGroup) {
  groupDialogRef.value?.open(group);
  groupDialogVisible.value = true;
}

// ---- Context Menu (composable) ----

const {
  ctxVisible, ctxStyle, ctxLink, ctxMenuRef,
  showContextMenu, ctxEdit, ctxDelete, ctxCopyLink, ctxToggleGroup,
  groupCtxVisible, groupCtxStyle, groupCtxMenuRef,
  showGroupContextMenu, groupCtxEdit, groupCtxDelete,
  onTouchStart, onTouchEnd, onTouchMove,
} = useBookmarkContextMenu(handleEditLink, handleDeleteLink, handleEditGroup);

// ---- Import / Export (composable) ----

const {
  quickUrl, quickLoading, handleQuickAdd,
  handleExport, handleImport, handleResetAll,
} = useBookmarkIO();

// ---- Helpers ----

function onDragEnd() {}

function getGroupNames(groupIds: string[]): string {
  return groupIds
    .map((gid) => bookmarkStore.groups.find((g) => g.id === gid)?.name || "未分类")
    .join(", ");
}

function getGroupName(groupId: string): string {
  return bookmarkStore.groups.find((g) => g.id === groupId)?.name || "未分类";
}
</script>

<template>
  <div class="bookmark-section" :class="{ 'bookmark-mobile': mobile }">
    <!-- 标题栏 -->
    <div v-if="!mobile" id="本地书签" class="bookmark-header">
      <div class="header-left">
        <m-icon icon="ion:bookmarks" color="#C71585" :size="22" />
        <h2>本地书签</h2>
        <span class="header-count">{{ bookmarkStore.totalCount }}</span>
      </div>
    </div>

    <!-- 分组标签 -->
    <div class="bookmark-group-tabs">
      <div class="group-tabs-scroll">
        <div
          class="group-tab"
          :class="{ active: !bookmarkStore.activeGroupId }"
          @click="bookmarkStore.setActiveGroup(null)"
        >
          全部
          <span class="tab-badge">{{ bookmarkStore.totalCount }}</span>
        </div>
        <div
          v-for="group in bookmarkStore.sortedGroups"
          :key="group.id"
          class="group-tab"
          :class="{ active: bookmarkStore.activeGroupId === group.id }"
          @click="bookmarkStore.setActiveGroup(group.id)"
          @contextmenu.prevent="showGroupContextMenu($event, group)"
          @dblclick.stop="handleEditGroup(group)"
        >
          <m-icon :icon="group.icon" :color="group.color" :size="15" />
          {{ group.name }}
          <span class="tab-badge">{{ bookmarkStore.groupCounts[group.id] || 0 }}</span>
        </div>
        <div class="group-tab tab-add" @click="handleAddGroup">
          <m-icon icon="mdi:plus" :size="14" />
        </div>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="bookmark-toolbar">
      <div class="toolbar-left">
        <el-radio-group
          :model-value="bookmarkStore.viewMode"
          size="small"
          @update:model-value="(v: any) => bookmarkStore.setViewMode(v)"
        >
          <el-radio-button value="grid">
            <m-icon icon="mdi:view-grid-outline" :size="14" />
          </el-radio-button>
          <el-radio-button value="compact">
            <m-icon icon="mdi:view-module-outline" :size="14" />
          </el-radio-button>
          <el-radio-button value="list">
            <m-icon icon="mdi:view-list-outline" :size="14" />
          </el-radio-button>
        </el-radio-group>

        <el-select
          :model-value="bookmarkStore.sortMode"
          size="small"
          style="width: 105px"
          @update:model-value="(v: any) => bookmarkStore.setSortMode(v)"
        >
          <el-option label="手动排序" value="manual" />
          <el-option label="最常访问" value="frequency" />
          <el-option label="最近访问" value="recent" />
          <el-option label="按名称" value="alpha" />
        </el-select>
      </div>

      <div class="toolbar-right">
        <el-popover trigger="click" :width="360" placement="bottom">
          <template #reference>
            <el-button size="small" type="success" plain>
              <m-icon icon="mdi:lightning-bolt" :size="14" class="mr-1" />快速添加
            </el-button>
          </template>
          <div class="flex gap-2">
            <el-input
              v-model="quickUrl"
              placeholder="粘贴链接，自动获取信息"
              size="small"
              @keyup.enter="handleQuickAdd"
            />
            <el-button type="primary" size="small" :loading="quickLoading" @click="handleQuickAdd">
              添加
            </el-button>
          </div>
        </el-popover>

        <el-button size="small" type="primary" @click="handleAddLink">
          <m-icon icon="mdi:plus" :size="14" class="mr-1" />添加
        </el-button>

        <el-dropdown trigger="click" @command="(cmd: string) => {
          if (cmd === 'import') handleImport();
          if (cmd === 'export') handleExport();
          if (cmd === 'clear') handleResetAll();
        }">
          <el-button size="small" plain circle>
            <m-icon icon="mdi:dots-horizontal" :size="16" />
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="import">
                <m-icon icon="mdi:import" :size="16" class="mr-2" />导入书签
              </el-dropdown-item>
              <el-dropdown-item command="export">
                <m-icon icon="mdi:export" :size="16" class="mr-2" />导出书签
              </el-dropdown-item>
              <el-dropdown-item command="clear" divided>
                <span class="text-red-500 flex items-center">
                  <m-icon icon="mdi:delete-sweep-outline" :size="16" class="mr-2" />清空所有
                </span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- ===================== 视图区 ===================== -->

    <bookmark-grid-view
      v-if="bookmarkStore.viewMode === 'grid'"
      :links="displayLinks"
      :all-links="bookmarkStore.links"
      :is-draggable="isDraggable"
      :mobile="mobile"
      :get-group-names="getGroupNames"
      @update:all-links="bookmarkStore.links = $event"
      @click="handleLinkClick"
      @edit="handleEditLink"
      @delete="(link) => { ctxLink = link; ctxDelete(); }"
      @contextmenu="showContextMenu"
      @drag-end="onDragEnd"
      @touchstart="onTouchStart"
      @touchend="onTouchEnd"
      @touchmove="onTouchMove"
    />

    <bookmark-compact-view
      v-else-if="bookmarkStore.viewMode === 'compact'"
      :links="displayLinks"
      :all-links="bookmarkStore.links"
      :is-draggable="isDraggable"
      :mobile="mobile"
      :get-group-names="getGroupNames"
      @update:all-links="bookmarkStore.links = $event"
      @click="handleLinkClick"
      @contextmenu="showContextMenu"
      @drag-end="onDragEnd"
      @touchstart="onTouchStart"
      @touchend="onTouchEnd"
      @touchmove="onTouchMove"
    />

    <bookmark-list-view
      v-else
      :links="displayLinks"
      :all-links="bookmarkStore.links"
      :is-draggable="isDraggable"
      :mobile="mobile"
      :get-group-names="getGroupNames"
      :get-group-name="getGroupName"
      @update:all-links="bookmarkStore.links = $event"
      @click="handleLinkClick"
      @edit="handleEditLink"
      @delete="(link) => { ctxLink = link; ctxDelete(); }"
      @contextmenu="showContextMenu"
      @drag-end="onDragEnd"
      @touchstart="onTouchStart"
      @touchend="onTouchEnd"
      @touchmove="onTouchMove"
    />

    <!-- 空状态 -->
    <div v-if="displayLinks.length === 0" class="bookmark-empty">
      <m-icon icon="mdi:bookmark-plus-outline" :size="48" class="empty-bk-icon" />
      <p>暂无书签</p>
      <el-button type="primary" size="small" @click="handleAddLink">添加第一个书签</el-button>
    </div>

    <!-- 书签右键菜单 -->
    <teleport to="body">
      <transition name="ctx-fade">
        <div v-show="ctxVisible" ref="ctxMenuRef" class="bk-ctx-menu" :style="ctxStyle">
          <div class="bk-ctx-item" @click="ctxEdit">
            <m-icon icon="mdi:pencil-outline" :size="16" />编辑
          </div>
          <div class="bk-ctx-item" @click="ctxCopyLink">
            <m-icon icon="mdi:content-copy" :size="16" />复制链接
          </div>
          <div class="bk-ctx-divider" v-if="bookmarkStore.groups.length > 1" />
          <template v-if="bookmarkStore.groups.length > 1">
            <div class="bk-ctx-label">所属分组（可多选）</div>
            <div
              v-for="g in bookmarkStore.sortedGroups"
              :key="g.id"
              class="bk-ctx-item bk-ctx-item-sm"
              :class="{ 'bk-ctx-item-active': ctxLink?.groupIds?.includes(g.id) }"
              @click="ctxToggleGroup(g.id)"
            >
              <m-icon
                :icon="ctxLink?.groupIds?.includes(g.id) ? 'mdi:checkbox-marked' : 'mdi:checkbox-blank-outline'"
                :color="ctxLink?.groupIds?.includes(g.id) ? 'var(--el-color-primary)' : ''"
                :size="14"
              />{{ g.name }}
            </div>
          </template>
          <div class="bk-ctx-divider" />
          <div class="bk-ctx-item bk-ctx-item-danger" @click="ctxDelete">
            <m-icon icon="mdi:trash-can-outline" :size="16" />删除
          </div>
        </div>
      </transition>
    </teleport>

    <!-- 分组标签右键菜单 -->
    <teleport to="body">
      <transition name="ctx-fade">
        <div v-show="groupCtxVisible" ref="groupCtxMenuRef" class="bk-ctx-menu" :style="groupCtxStyle">
          <div class="bk-ctx-item" @click="groupCtxEdit">
            <m-icon icon="mdi:pencil-outline" :size="16" />编辑分组
          </div>
          <div class="bk-ctx-divider" />
          <div class="bk-ctx-item bk-ctx-item-danger" @click="groupCtxDelete">
            <m-icon icon="mdi:trash-can-outline" :size="16" />删除分组
          </div>
        </div>
      </transition>
    </teleport>

    <!-- 对话框 -->
    <m-local-add-link ref="linkRef" v-model="linkDialogVisible" />
    <bookmark-group-dialog ref="groupDialogRef" v-model="groupDialogVisible" />
  </div>
</template>

<style lang="scss" scoped>
.bookmark-section {
  margin-bottom: 28px;
}

// ---- Header ----
.bookmark-header {
  margin-bottom: 14px;

  .header-left {
    display: flex;
    align-items: center;
    gap: 8px;

    h2 {
      font-size: 1.15rem;
      font-weight: 700;
      margin: 0;
    }

    .header-count {
      font-size: 12px;
      color: #fff;
      background: var(--el-color-primary);
      border-radius: 10px;
      padding: 1px 8px;
      line-height: 1.4;
    }
  }
}

// ---- Group Tabs ----
.bookmark-group-tabs {
  margin-bottom: 12px;
  overflow-x: auto;
  &::-webkit-scrollbar { height: 0; }
}

.group-tabs-scroll {
  display: flex;
  gap: 6px;
  white-space: nowrap;
}

.group-tab {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 14px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  background-color: var(--nav-card-bg);
  color: var(--nav-text-secondary);
  transition: all 0.18s ease;
  user-select: none;
  border: 1px solid transparent;

  &:hover {
    color: var(--el-color-primary);
    border-color: var(--el-color-primary-light-7);
  }

  &.active {
    background-color: var(--el-color-primary-light-9);
    color: var(--el-color-primary);
    border-color: var(--el-color-primary-light-5);
    font-weight: 600;
  }

  .tab-badge {
    font-size: 11px;
    background: var(--el-fill-color);
    border-radius: 8px;
    padding: 0 5px;
    line-height: 1.5;
  }

  &.active .tab-badge {
    background: var(--el-color-primary-light-7);
    color: var(--el-color-primary);
  }

  &.tab-add {
    border: 1px dashed var(--el-border-color-light);
    background: transparent;
    padding: 5px 10px;
    &:hover {
      border-color: var(--el-color-primary);
      color: var(--el-color-primary);
    }
  }
}

// ---- Toolbar ----
.bookmark-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

// ---- Empty State ----
.bookmark-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0 36px;
  gap: 10px;
  color: var(--nav-text-secondary);
  font-size: 13px;

  .empty-bk-icon {
    color: var(--el-border-color-light, #dcdfe6);
  }
}

// ---- Mobile ----
.bookmark-mobile {
  .bookmark-toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  .toolbar-left,
  .toolbar-right {
    justify-content: center;
  }

  .bookmark-group-tabs {
    margin-bottom: 10px;
    -webkit-overflow-scrolling: touch;
  }

  .group-tab {
    padding: 4px 10px;
    font-size: 12px;
  }
}
</style>

<!-- Context menu styles: unscoped because teleport renders outside component DOM -->
<style lang="scss">
.bk-ctx-menu {
  position: fixed;
  z-index: 9999;
  min-width: 160px;
  padding: 6px 0;
  background: var(--nav-card-bg, #fff);
  border-radius: 8px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.04);
}

.bk-ctx-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.12s;
  color: var(--nav-text);

  &:hover { background: var(--el-fill-color-lighter); }

  &.bk-ctx-item-sm {
    padding: 5px 14px 5px 22px;
    font-size: 12px;
  }

  &.bk-ctx-item-active {
    color: var(--el-color-primary);
    font-weight: 600;
  }

  &.bk-ctx-item-danger {
    color: var(--el-color-danger);
    &:hover { background: var(--el-color-danger-light-9); }
  }
}

.bk-ctx-label {
  padding: 4px 14px 2px;
  font-size: 11px;
  color: var(--nav-text-secondary);
  user-select: none;
}

.bk-ctx-divider {
  height: 1px;
  margin: 4px 8px;
  background: var(--el-border-color-lighter);
}

.ctx-fade-enter-active { transition: opacity 0.12s, transform 0.12s; }
.ctx-fade-leave-active { transition: opacity 0.08s; }
.ctx-fade-enter-from { opacity: 0; transform: scale(0.95); }
.ctx-fade-leave-to { opacity: 0; }
</style>
