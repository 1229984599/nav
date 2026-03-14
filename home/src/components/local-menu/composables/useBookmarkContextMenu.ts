import { nextTick, onBeforeUnmount, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useBookmarkStore } from "@/store/bookmark";
import type { LocalLink, BookmarkGroup } from "@/types/bookmark";
import { DEFAULT_GROUP_ID } from "@/types/bookmark";

export function useBookmarkContextMenu(
  handleEditLink: (link: LocalLink) => void,
  handleDeleteLink: (link: LocalLink) => void,
  handleEditGroup: (group: BookmarkGroup) => void
) {
  const bookmarkStore = useBookmarkStore();

  // Link context menu
  const ctxVisible = ref(false);
  const ctxStyle = ref({ left: "0px", top: "0px" });
  const ctxLink = ref<LocalLink | null>(null);
  const ctxMenuRef = ref<HTMLElement | null>(null);

  // Group context menu
  const groupCtxVisible = ref(false);
  const groupCtxStyle = ref({ left: "0px", top: "0px" });
  const groupCtxTarget = ref<BookmarkGroup | null>(null);
  const groupCtxMenuRef = ref<HTMLElement | null>(null);

  function onDocMouseDown(e: MouseEvent) {
    const target = e.target as HTMLElement;
    if (ctxMenuRef.value?.contains(target) || groupCtxMenuRef.value?.contains(target)) return;
    hideContextMenu();
    hideGroupCtx();
  }

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

  // Group context menu
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

  // Mobile long-press support
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

  return {
    // Link context menu
    ctxVisible, ctxStyle, ctxLink, ctxMenuRef,
    showContextMenu, hideContextMenu, ctxEdit, ctxDelete, ctxCopyLink, ctxToggleGroup,
    // Group context menu
    groupCtxVisible, groupCtxStyle, groupCtxTarget, groupCtxMenuRef,
    showGroupContextMenu, hideGroupCtx, groupCtxEdit, groupCtxDelete,
    // Mobile touch
    onTouchStart, onTouchEnd, onTouchMove,
  };
}
