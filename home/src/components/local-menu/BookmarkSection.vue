<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref } from "vue";
import { VueDraggable } from "vue-draggable-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import MIcon from "@/components/MIcon.vue";
import MLocalAddLink from "@/components/add-link/local.vue";
import BookmarkGroupDialog from "./BookmarkGroupDialog.vue";
import { useBookmarkStore } from "@/store/bookmark";
import { DEFAULT_GROUP_ID } from "@/types/bookmark";
import type { LocalLink, BookmarkGroup, BookmarkExportData } from "@/types/bookmark";
import linksModel from "@/api/links";
import { isUrl } from "@/utils/window";

defineOptions({ name: "BookmarkSection" });

const props = withDefaults(defineProps<{ mobile?: boolean }>(), { mobile: false });

const bookmarkStore = useBookmarkStore();
const linkDialogVisible = ref(false);
const linkRef = ref<InstanceType<typeof MLocalAddLink>>();
const groupDialogRef = ref<InstanceType<typeof BookmarkGroupDialog>>();
const groupDialogVisible = ref(false);

// 快速添加
const quickUrl = ref("");
const quickLoading = ref(false);

// 右键菜单
const ctxVisible = ref(false);
const ctxStyle = ref({ left: "0px", top: "0px" });
const ctxLink = ref<LocalLink | null>(null);

// 分组标签右键
const groupCtxVisible = ref(false);
const groupCtxStyle = ref({ left: "0px", top: "0px" });
const groupCtxTarget = ref<BookmarkGroup | null>(null);

// ---- Computed ----

const displayLinks = computed(() => bookmarkStore.activeLinks);
const isDraggable = computed(() => bookmarkStore.sortMode === "manual");

// ---- 右键菜单 ----

const ctxMenuRef = ref<HTMLElement | null>(null);
const groupCtxMenuRef = ref<HTMLElement | null>(null);

function showContextMenu(e: MouseEvent, link: LocalLink) {
  e.preventDefault();
  ctxLink.value = link;
  ctxStyle.value = { left: `${e.clientX}px`, top: `${e.clientY}px` };
  ctxVisible.value = true;
  groupCtxVisible.value = false;
  document.removeEventListener("mousedown", onDocMouseDown);
  nextTick(() => {
    document.addEventListener("mousedown", onDocMouseDown);
  });
}

function hideContextMenu() {
  ctxVisible.value = false;
  document.removeEventListener("mousedown", onDocMouseDown);
}

function onDocMouseDown(e: MouseEvent) {
  const target = e.target as HTMLElement;
  if (ctxMenuRef.value?.contains(target) || groupCtxMenuRef.value?.contains(target)) return;
  hideContextMenu();
  hideGroupCtx();
}

function ctxEdit() {
  if (!ctxLink.value) return;
  handleEditLink(ctxLink.value);
  ctxVisible.value = false;
}

function ctxDelete() {
  if (!ctxLink.value) return;
  const link = ctxLink.value;
  hideContextMenu();
  ElMessageBox.confirm("确定要删除该书签？", "删除确认", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
    confirmButtonClass: "el-button--danger",
  }).then(() => {
    handleDeleteLink(link);
  });
}

function ctxCopyLink() {
  if (!ctxLink.value) return;
  navigator.clipboard.writeText(ctxLink.value.href).then(() => {
    ElMessage.success("链接已复制");
  });
  ctxVisible.value = false;
}

function ctxToggleGroup(groupId: string) {
  if (!ctxLink.value) return;
  bookmarkStore.toggleLinkGroup(ctxLink.value.id, groupId);
}

// 分组标签右键

function showGroupContextMenu(e: MouseEvent, group: BookmarkGroup) {
  e.preventDefault();
  if (group.id === DEFAULT_GROUP_ID) return;
  groupCtxTarget.value = group;
  groupCtxStyle.value = { left: `${e.clientX}px`, top: `${e.clientY}px` };
  groupCtxVisible.value = true;
  ctxVisible.value = false;
  document.removeEventListener("mousedown", onDocMouseDown);
  nextTick(() => {
    document.addEventListener("mousedown", onDocMouseDown);
  });
}

function hideGroupCtx() {
  groupCtxVisible.value = false;
  document.removeEventListener("mousedown", onDocMouseDown);
}

function groupCtxEdit() {
  if (!groupCtxTarget.value) return;
  handleEditGroup(groupCtxTarget.value);
  groupCtxVisible.value = false;
}

function groupCtxDelete() {
  if (!groupCtxTarget.value) return;
  const g = groupCtxTarget.value;
  hideGroupCtx();
  ElMessageBox.confirm(
    `删除分组「${g.name}」后，其下书签将移至未分类。`,
    "删除确认",
    { confirmButtonText: "删除", cancelButtonText: "取消", type: "warning", confirmButtonClass: "el-button--danger" }
  ).then(() => {
    bookmarkStore.deleteGroup(g.id);
    ElMessage.success("分组已删除");
  });
}

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

// ---- Quick Add ----

async function handleQuickAdd() {
  if (!quickUrl.value || !isUrl(quickUrl.value)) {
    ElMessage.warning("请输入有效的URL");
    return;
  }
  quickLoading.value = true;
  try {
    const data: any = await linksModel.getSiteInfo(quickUrl.value);
    bookmarkStore.addLink({
      href: quickUrl.value,
      title: data?.title || new URL(quickUrl.value).hostname,
      icon: data?.icon || "",
      color: data?.color || "",
      desc: data?.desc || "",
      is_self: false,
      groupIds: [bookmarkStore.activeGroupId || DEFAULT_GROUP_ID],
    });
    ElMessage.success("添加成功");
    quickUrl.value = "";
  } catch {
    bookmarkStore.addLink({
      href: quickUrl.value,
      title: new URL(quickUrl.value).hostname,
      icon: "",
      color: "",
      desc: "",
      is_self: false,
      groupIds: [bookmarkStore.activeGroupId || DEFAULT_GROUP_ID],
    });
    ElMessage.success("添加成功（未能采集到站点信息）");
    quickUrl.value = "";
  } finally {
    quickLoading.value = false;
  }
}

// ---- Import / Export ----

function handleExport() {
  const data = bookmarkStore.exportData();
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `bookmarks-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
  ElMessage.success("导出成功");
}

function handleImport() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";
  input.onchange = async (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    try {
      const text = await file.text();
      const data: BookmarkExportData = JSON.parse(text);
      if (data.version !== 1 || !Array.isArray(data.groups) || !Array.isArray(data.links)) {
        throw new Error("Invalid format");
      }
      ElMessageBox.confirm("选择导入方式", "导入书签", {
        confirmButtonText: "替换全部",
        cancelButtonText: "合并追加",
        distinguishCancelAndClose: true,
      })
        .then(() => {
          bookmarkStore.importData(data, "replace");
          ElMessage.success("导入成功（替换）");
        })
        .catch((action: string) => {
          if (action === "cancel") {
            bookmarkStore.importData(data, "merge");
            ElMessage.success("导入成功（合并）");
          }
        });
    } catch {
      ElMessage.error("文件格式错误");
    }
  };
  input.click();
}

function handleResetAll() {
  ElMessageBox.confirm("确定要清空所有本地书签吗？此操作不可恢复。", "清空确认", {
    confirmButtonText: "清空",
    cancelButtonText: "取消",
    type: "error",
    confirmButtonClass: "el-button--danger",
  }).then(() => {
    bookmarkStore.resetAll();
    ElMessage.success("清空成功");
  });
}

function onDragEnd() {}

function getGroupNames(groupIds: string[]): string {
  return groupIds
    .map((gid) => bookmarkStore.groups.find((g) => g.id === gid)?.name || "未分类")
    .join(", ");
}

function getGroupName(groupId: string): string {
  return bookmarkStore.groups.find((g) => g.id === groupId)?.name || "未分类";
}

// ---- 移动端长按支持 ----
let longPressTimer: ReturnType<typeof setTimeout> | null = null;

function onTouchStart(e: TouchEvent, link: LocalLink) {
  longPressTimer = setTimeout(() => {
    longPressTimer = null;
    const touch = e.touches[0];
    ctxLink.value = link;
    ctxStyle.value = { left: `${touch.clientX}px`, top: `${touch.clientY}px` };
    ctxVisible.value = true;
    groupCtxVisible.value = false;
    document.removeEventListener("mousedown", onDocMouseDown);
    nextTick(() => {
      document.addEventListener("mousedown", onDocMouseDown);
    });
  }, 500);
}

function onTouchEnd() {
  if (longPressTimer) {
    clearTimeout(longPressTimer);
    longPressTimer = null;
  }
}

function onTouchMove() {
  if (longPressTimer) {
    clearTimeout(longPressTimer);
    longPressTimer = null;
  }
}

onBeforeUnmount(() => {
  document.removeEventListener("mousedown", onDocMouseDown);
  if (longPressTimer) clearTimeout(longPressTimer);
});
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

    <!-- Grid 视图 -->
    <VueDraggable
      v-if="bookmarkStore.viewMode === 'grid'"
      v-model="bookmarkStore.links"
      class="bookmark-grid"
      :class="mobile
        ? 'grid-cols-2 lg:grid-cols-3'
        : 'grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5'"
      :disabled="!isDraggable"
      :animation="200"
      ghost-class="drag-ghost"
      @end="onDragEnd"
    >
      <template v-for="link in displayLinks" :key="link.id">
        <div
          class="card-wrap"
          @contextmenu="showContextMenu($event, link)"
          @touchstart.passive="mobile && onTouchStart($event, link)"
          @touchend.passive="onTouchEnd()"
          @touchmove.passive="onTouchMove()"
        >
          <a
            class="bk-card"
            :href="link.href"
            :target="link.is_self ? '_self' : '_blank'"
            @click="handleLinkClick(link)"
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
              <span class="bar-btn" title="编辑" @click.stop.prevent="handleEditLink(link)">
                <m-icon icon="mdi:pencil-outline" :size="14" />
              </span>
              <span class="bar-btn bar-btn-danger" title="删除" @click.stop.prevent="ctxLink = link; ctxDelete()">
                <m-icon icon="mdi:trash-can-outline" :size="14" />
              </span>
            </div>
          </div>
        </div>
      </template>
    </VueDraggable>

    <!-- Compact 视图 -->
    <VueDraggable
      v-else-if="bookmarkStore.viewMode === 'compact'"
      v-model="bookmarkStore.links"
      class="bookmark-compact"
      :class="mobile
        ? 'grid-cols-4 lg:grid-cols-5 xl:grid-cols-6'
        : 'grid-cols-5 lg:grid-cols-7 xl:grid-cols-9 2xl:grid-cols-11'"
      :disabled="!isDraggable"
      :animation="200"
      ghost-class="drag-ghost"
      @end="onDragEnd"
    >
      <template v-for="link in displayLinks" :key="link.id">
        <a
          class="compact-item"
          :href="link.href"
          :target="link.is_self ? '_self' : '_blank'"
          @click="handleLinkClick(link)"
          @contextmenu="showContextMenu($event, link)"
          @touchstart.passive="mobile && onTouchStart($event, link)"
          @touchend.passive="onTouchEnd()"
          @touchmove.passive="onTouchMove()"
        >
          <div class="compact-icon">
            <m-icon :icon="link.icon" :color="link.color" :size="32" />
          </div>
          <span class="compact-title">{{ link.title }}</span>
          <span class="compact-group">{{ getGroupNames(link.groupIds) }}</span>
        </a>
      </template>
    </VueDraggable>

    <!-- List 视图 -->
    <VueDraggable
      v-else
      v-model="bookmarkStore.links"
      class="bookmark-list"
      :disabled="!isDraggable"
      :animation="200"
      ghost-class="drag-ghost"
      @end="onDragEnd"
    >
      <template v-for="link in displayLinks" :key="link.id">
        <div
          class="list-row"
          @contextmenu="showContextMenu($event, link)"
          @touchstart.passive="mobile && onTouchStart($event, link)"
          @touchend.passive="onTouchEnd()"
          @touchmove.passive="onTouchMove()"
        >
          <a
            class="list-link"
            :href="link.href"
            :target="link.is_self ? '_self' : '_blank'"
            @click="handleLinkClick(link)"
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
            <span class="list-action" title="编辑" @click.stop="handleEditLink(link)">
              <m-icon icon="mdi:pencil-outline" :size="15" />
            </span>
            <span class="list-action list-action-danger" title="删除" @click.stop="ctxLink = link; ctxDelete()">
              <m-icon icon="mdi:trash-can-outline" :size="15" />
            </span>
          </div>
        </div>
      </template>
    </VueDraggable>

    <!-- 空状态 -->
    <div v-if="displayLinks.length === 0" class="bookmark-empty">
      <m-icon icon="mdi:bookmark-plus-outline" :size="48" color="#dcdfe6" />
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

// ---- Drag Ghost ----
.drag-ghost {
  opacity: 0.4;
}

// ========== Grid View ==========
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
    left: 0;
    top: 0;
    bottom: 0;
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
    top: 8px;
    right: 10px;
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
    width: 22px;
    height: 22px;
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

// ========== Compact View ==========
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
    width: 44px;
    height: 44px;
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

// ========== List View ==========
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
    width: 24px;
    height: 24px;
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
  .bk-card {
    padding: 10px 10px 8px;
    .card-title { font-size: 0.85rem; }
  }

  // 移动端：操作按钮始终可见（无 hover）
  .bar-actions {
    opacity: 1 !important;
  }
  .list-action {
    opacity: 1 !important;
  }

  // 移动端卡片间距更紧凑
  .bookmark-grid {
    gap: 10px;
  }

  // 移动端分组标签横向滚动
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
  background: #fff;
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
