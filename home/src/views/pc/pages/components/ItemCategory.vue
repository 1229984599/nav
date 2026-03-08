<script setup lang="ts">
import ItemDesc from "./ItemDesc.vue";
import MIcon from "@/components/MIcon.vue";
import { computed, PropType, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { MenuSchemaTree } from "@/api/menu/types";
import { LinkSchemaList } from "@/api/links/types";
import { VueDraggable } from "vue-draggable-plus";
import { useUserStore } from "@/store/user";
import links from "@/api/links";
import LinkContextMenu from "@/components/link-context-menu/index.vue";
import EmptyState from "@/components/EmptyState.vue";

const userStore = useUserStore();

const props = defineProps({
  menu: {
    type: Object as PropType<MenuSchemaTree>,
  },
});

const isAdmin = computed(() => userStore.isAdminAuthorized);
const linkList = ref<LinkSchemaList[]>([]);
const contextMenuRef = ref<InstanceType<typeof LinkContextMenu>>();
const orderSaving = ref(false);
const dragSnapshot = ref<LinkSchemaList[]>([]);

watch(
  () => props.menu?.links,
  (val) => {
    linkList.value = val ? [...val] : [];
  },
  { immediate: true },
);

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

function handleLinkDragStart() {
  dragSnapshot.value = linkList.value.map((item) => ({ ...item }));
}

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
  </div>
  <VueDraggable
    v-if="isAdmin"
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
