<script setup lang="ts">
import ItemDesc from "./ItemDesc.vue";
import MIcon from "@/components/MIcon.vue";
import { computed, nextTick, onBeforeUnmount, PropType, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { MenuSchemaTree } from "@/api/menu/types";
import { LinkSchemaList } from "@/api/links/types";
import { VueDraggable } from "vue-draggable-plus";
import { useUserStore } from "@/store/user";
import { isMobile } from "@/utils/window";
import { useMenuStore } from "@/store/menu";
import links from "@/api/links";
import menuApi from "@/api/menu";
import LinkContextMenu from "@/components/link-context-menu/index.vue";
import MenuContextMenu from "@/components/menu-context-menu/index.vue";
import EmptyState from "@/components/EmptyState.vue";

const userStore = useUserStore();
const menuStore = useMenuStore();
const route = useRoute();
const router = useRouter();

const props = defineProps({
  menu: {
    type: Object as PropType<MenuSchemaTree>,
  },
});

const isAdmin = computed(() => userStore.isAdminAuthorized);
const editMode = ref(false);
const isDragActive = computed(
  () => isAdmin.value && (!isMobile.value || editMode.value),
);
const contextMenuRef = ref<InstanceType<typeof LinkContextMenu>>();
const menuContextMenuRef = ref<InstanceType<typeof MenuContextMenu>>();
const tabPillsWrapperRef = ref<HTMLElement>();
const orderSaving = ref(false);
const tabOrderSaving = ref(false);
const dragSnapshot = ref<LinkSchemaList[]>([]);

type TabItem = {
  key: string;
  title: string;
  menu: MenuSchemaTree;
  isParent: boolean;
};

// 将选中的 tab pill 滚动到可见区域
function scrollActiveTabIntoView() {
  nextTick(() => {
    const wrapper = tabPillsWrapperRef.value;
    if (!wrapper) return;
    const activeEl = wrapper.querySelector<HTMLElement>(".tab-pill.active");
    if (!activeEl) return;
    const pillRect = activeEl.getBoundingClientRect();
    const scrollLeft =
      activeEl.offsetLeft - wrapper.offsetWidth / 2 + pillRect.width / 2;
    wrapper.scrollTo({ left: Math.max(0, scrollLeft), behavior: "smooth" });
  });
}

// Build tabs: parent itself (if it has links) + all children
const tabs = computed(() => {
  const result: TabItem[] = [];
  if (props.menu) {
    // Add parent as first tab if it has its own links
    if (props.menu.links && props.menu.links.length > 0) {
      result.push({
        key: "parent-" + props.menu.id,
        title: props.menu.title || "",
        menu: props.menu,
        isParent: true,
      });
    }
    // Add children as tabs
    if (props.menu.children) {
      for (const child of props.menu.children) {
        if (child.status !== false) {
          result.push({
            key: "child-" + child.id,
            title: child.title || "",
            menu: child,
            isParent: false,
          });
        }
      }
    }
  }
  return result;
});

// 可拖拽的 tab 列表（admin 模式下使用）
const tabList = ref<TabItem[]>([]);

watch(
  tabs,
  (val) => {
    // 仅在非拖拽排序保存中同步
    if (!tabOrderSaving.value) {
      tabList.value = [...val];
    }
  },
  { immediate: true },
);

// Active tab key
const activeTab = ref("");

// Initialize active tab (check URL sub param first)
watch(
  tabs,
  (val) => {
    if (val.length > 0 && !val.find((t) => t.key === activeTab.value)) {
      // 首次初始化：检查 URL 中的 sub 参数
      const urlSub = route.query?.sub;
      const urlCat = route.query?.cat;
      if (
        urlSub &&
        typeof urlSub === "string" &&
        urlCat === props.menu?.title
      ) {
        const matchTab = val.find((t) => t.title === urlSub);
        if (matchTab) {
          activeTab.value = matchTab.key;
          return;
        }
      }
      activeTab.value = val[0].key;
    }
  },
  { immediate: true },
);

// Listen for sidebar sub-tab activation
watch(
  () => menuStore.activeSubTab,
  (val) => {
    if (!val || val.parentId !== props.menu?.id) return;
    const targetKey = "child-" + val.childId;
    if (tabs.value.find((t) => t.key === targetKey)) {
      activeTab.value = targetKey;
    }
    // 延迟清除，确保所有 TabCategory 实例的 watcher 都已处理
    nextTick(() => {
      if (menuStore.activeSubTab === val) {
        menuStore.clearActiveSubTab();
      }
    });
  },
);

// 监听路由变化：点击父分类时（无 sub），切回第一个 tab 显示父类数据
watch(
  () => ({ cat: route.query?.cat, sub: route.query?.sub, _t: route.query?._t }),
  ({ cat, sub }) => {
    if (cat === props.menu?.title && !sub && tabs.value.length > 0) {
      activeTab.value = tabs.value[0].key;
    }
  },
);

// Current active menu based on selected tab
const activeMenu = computed(() => {
  const tab = tabs.value.find((t) => t.key === activeTab.value);
  return tab?.menu;
});

// activeTab 变化时，滚动 tab pill 到可见区域（移动端）+ 同步侧边栏高亮
watch(activeTab, (key) => {
  scrollActiveTabIntoView();
  // 同步侧边栏菜单高亮
  const tab =
    tabs.value.find((t) => t.key === key) ||
    tabList.value.find((t) => t.key === key);
  if (tab) {
    menuStore.setActiveMenuIndex(tab.title);
  }
});

// 用户点击 tab 时，切换 activeTab 并同步 URL
function handleTabClick(tab: TabItem) {
  activeTab.value = tab.key;
  // 同步 URL sub 参数，刷新页面时恢复正确的 tab
  const query: Record<string, string> = { cat: props.menu?.title || "" };
  if (!tab.isParent) {
    query.sub = tab.title;
  }
  router.replace({ path: "/list", query });
}

// Draggable link list for admin mode
const linkList = ref<LinkSchemaList[]>([]);

// Tab 拖拽排序相关
const tabDragSnapshot = ref<TabItem[]>([]);

function handleTabDragStart() {
  tabDragSnapshot.value = tabList.value.map((t) => ({ ...t }));
}

async function handleTabDragEnd() {
  if (tabOrderSaving.value) return;
  // 只对子分类 tab 保存排序（父分类 tab 不参与排序）
  const childTabs = tabList.value.filter((t) => !t.isParent);
  const updates = childTabs
    .filter((t) => t.menu.id)
    .map((t, index) => ({
      id: t.menu.id!,
      order: index,
    }));
  if (updates.length === 0) return;
  tabOrderSaving.value = true;
  try {
    await menuApi.batchUpdate(updates);
    // 同步更新 menuTree 中 children 的顺序
    if (props.menu?.children) {
      const orderMap = new Map(updates.map((u) => [u.id, u.order]));
      props.menu.children.sort(
        (a, b) => (orderMap.get(a.id!) ?? 0) - (orderMap.get(b.id!) ?? 0),
      );
    }
    ElMessage.success("分类排序已保存");
  } catch (e) {
    tabList.value = tabDragSnapshot.value.map((t) => ({ ...t }));
    ElMessage.error("分类排序保存失败，已恢复原顺序");
    console.error("分类排序保存失败", e);
  } finally {
    tabOrderSaving.value = false;
    tabDragSnapshot.value = [];
  }
}

watch(
  () => activeMenu.value?.links,
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

// Tab 右键菜单（桌面端）
function handleTabContextMenu(event: MouseEvent, tab: TabItem) {
  if (!isAdmin.value || tab.isParent) return;
  event.preventDefault();
  menuContextMenuRef.value?.show(event, tab.menu);
}

// Tab 长按菜单（移动端）
const longPressTimer = ref<ReturnType<typeof setTimeout>>();

function handleTabTouchStart(event: TouchEvent, tab: TabItem) {
  if (!isAdmin.value || tab.isParent) return;
  longPressTimer.value = setTimeout(() => {
    menuContextMenuRef.value?.show(event, tab.menu);
  }, 500);
}

function handleTabTouchEnd() {
  if (longPressTimer.value) {
    clearTimeout(longPressTimer.value);
    longPressTimer.value = undefined;
  }
}

onBeforeUnmount(() => {
  if (longPressTimer.value) {
    clearTimeout(longPressTimer.value);
    longPressTimer.value = undefined;
  }
});
</script>

<template>
  <div :id="menu?.title" role="region" :aria-label="menu?.title">
    <!-- Header: icon + title + tab pills -->
    <div class="category-header">
      <div class="category-title-row">
        <m-icon
          v-if="menu?.icon"
          :style="{ color: menu?.color }"
          :icon="menu.icon"
        />
        <h2 class="text-xl font-bold whitespace-nowrap">{{ menu?.title }}</h2>
        <button
          v-if="isAdmin && isMobile"
          class="edit-mode-btn"
          :class="{ active: editMode }"
          @click="editMode = !editMode"
        >
          <m-icon
            :icon="editMode ? 'mdi:check' : 'mdi:sort-variant'"
            :size="14"
          />
          {{ editMode ? "完成" : "排序" }}
        </button>
      </div>

      <!-- Tab pills -->
      <div ref="tabPillsWrapperRef" class="tab-pills-wrapper">
        <!-- Admin: draggable tabs -->
        <VueDraggable
          v-if="isDragActive"
          v-model="tabList"
          :disabled="tabOrderSaving"
          class="tab-pills"
          :animation="200"
          ghost-class="tab-drag-ghost"
          @start="handleTabDragStart"
          @end="handleTabDragEnd"
        >
          <button
            v-for="tab in tabList"
            :key="tab.key"
            :class="['tab-pill', { active: activeTab === tab.key }]"
            @click="handleTabClick(tab)"
            @contextmenu="handleTabContextMenu($event, tab)"
            @touchstart.passive="handleTabTouchStart($event, tab)"
            @touchend="handleTabTouchEnd"
            @touchmove="handleTabTouchEnd"
          >
            {{ tab.title }}
          </button>
        </VueDraggable>
        <!-- Normal: plain tabs -->
        <div v-else class="tab-pills" role="tablist">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            :class="['tab-pill', { active: activeTab === tab.key }]"
            role="tab"
            :aria-selected="activeTab === tab.key"
            @click="handleTabClick(tab)"
          >
            {{ tab.title }}
          </button>
        </div>
      </div>
    </div>

    <!-- Link cards grid -->
    <transition name="fade-slide" mode="out-in">
      <div :key="activeTab">
        <VueDraggable
          v-if="isDragActive && linkList.length > 0"
          v-model="linkList"
          :disabled="orderSaving"
          class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mb-8"
          :animation="200"
          ghost-class="drag-ghost"
          @start="handleLinkDragStart"
          @end="handleLinkDragEnd"
        >
          <item-desc
            :item="item"
            v-for="item in linkList"
            :key="item.id"
            @contextmenu="handleItemContextMenu"
          />
        </VueDraggable>
        <div
          v-else-if="activeMenu?.links && activeMenu.links.length > 0"
          class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mb-8"
        >
          <item-desc
            :item="item"
            v-for="item in activeMenu?.links"
            :key="item.id"
          />
        </div>
        <empty-state
          v-else
          icon="mdi:link-off"
          text="该分类暂无链接"
          class="mb-8"
        />
      </div>
    </transition>
  </div>
  <link-context-menu v-if="isAdmin" ref="contextMenuRef" />
  <menu-context-menu v-if="isAdmin" ref="menuContextMenuRef" />
</template>

<style lang="scss" scoped>
.category-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;

  @media screen and (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}

.category-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.tab-pills-wrapper {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  background: var(--nav-card-bg, #fff);
  border-radius: 10px;
  padding: 5px 6px;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.04),
    0 0 0 1px var(--nav-border, rgba(0, 0, 0, 0.06));

  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;
  scrollbar-width: none;

  @media screen and (max-width: 768px) {
    width: 100%;
  }
}

.tab-pills {
  display: flex;
  gap: 2px;
  white-space: nowrap;
}

.tab-pill {
  position: relative;
  padding: 4px 14px;
  font-size: 0.8125rem;
  color: var(--nav-text-secondary, #6b7280);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 7px;
  line-height: 1.5;
  flex-shrink: 0;
  letter-spacing: 0.01em;

  &:hover {
    color: var(--el-color-primary, #409eff);
    background-color: var(--el-color-primary-light-9, rgba(64, 158, 255, 0.08));
  }

  &.active {
    color: #fff;
    background: linear-gradient(
      135deg,
      var(--el-color-primary, #409eff),
      var(--el-color-primary-light-3, #66b1ff)
    );
    font-weight: 500;
    box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
  }
}

.tab-drag-ghost {
  opacity: 0.4;
}

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
