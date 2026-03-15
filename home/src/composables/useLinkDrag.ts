import { computed, ref, watch, type Ref, type WatchSource } from "vue";
import { ElMessage } from "element-plus";
import { LinkSchemaList } from "@/api/links/types";
import { useUserStore } from "@/store/user";
import { isMobile } from "@/utils/window";
import links from "@/api/links";

/**
 * Shared composable for link drag-and-drop reordering.
 * Used by both ItemCategory and TabCategory.
 *
 * @param linksSource - reactive getter for the current link list
 */
export function useLinkDrag(linksSource: WatchSource<LinkSchemaList[] | undefined>) {
  const userStore = useUserStore();

  const isAdmin = computed(() => userStore.isAdminAuthorized);
  const editMode = ref(false);
  const isDragActive = computed(() => isAdmin.value && (!isMobile.value || editMode.value));
  const linkList = ref<LinkSchemaList[]>([]);
  const orderSaving = ref(false);
  const dragSnapshot = ref<LinkSchemaList[]>([]);

  watch(
    linksSource,
    (val) => {
      linkList.value = val ? [...val] : [];
    },
    { immediate: true },
  );

  function handleLinkDragStart() {
    dragSnapshot.value = linkList.value.map((item) => ({ ...item }));
  }

  async function handleLinkDragEnd() {
    if (orderSaving.value) return;
    const updates = linkList.value
      .filter((item) => item.id)
      .map((item, index) => ({
        id: item.id!,
        order: index,
      }));
    if (updates.length === 0) return;
    orderSaving.value = true;
    try {
      await links.batchUpdate(updates);
      ElMessage.success("链接排序已保存");
    } catch (e) {
      linkList.value = dragSnapshot.value.map((item) => ({ ...item }));
      ElMessage.error("链接排序保存失败，已恢复原顺序");
      console.error("链接排序保存失败", e);
    } finally {
      orderSaving.value = false;
      dragSnapshot.value = [];
    }
  }

  return {
    isAdmin,
    editMode,
    isDragActive,
    linkList,
    orderSaving,
    handleLinkDragStart,
    handleLinkDragEnd,
  };
}
