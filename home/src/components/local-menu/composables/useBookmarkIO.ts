import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useBookmarkStore } from "@/store/bookmark";
import { DEFAULT_GROUP_ID } from "@/types/bookmark";
import type { BookmarkExportData } from "@/types/bookmark";
import linksModel from "@/api/links";
import { isUrl } from "@/utils/window";

export function useBookmarkIO() {
  const bookmarkStore = useBookmarkStore();

  // Quick add
  const quickUrl = ref("");
  const quickLoading = ref(false);

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

  // Export
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

  // Import
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

  // Reset
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

  return {
    quickUrl, quickLoading, handleQuickAdd,
    handleExport, handleImport, handleResetAll,
  };
}
