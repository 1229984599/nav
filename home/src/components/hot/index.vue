<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { computed, defineAsyncComponent, nextTick, ref, watch } from "vue";
import { isMobile } from "@/utils/window";
const VueDraggable = defineAsyncComponent(() =>
  import("vue-draggable-plus").then((m) => m.VueDraggable)
);
import MHotItem from "./HotItem.vue";

defineOptions({
  name: "MHot",
});
defineProps({
  color: {
    type: String,
    default: "rgb(75 85 99 /)",
  },
});

// 全部支持的平台列表（name = pearktrue API 的 title 参数）
interface HotPlatform {
  label: string;
  name: string;
}

const ALL_PLATFORMS: HotPlatform[] = [
  { label: "36氪", name: "36氪" },
  { label: "51CTO", name: "51CTO" },
  { label: "吾爱破解", name: "吾爱破解" },
  { label: "AcFun", name: "AcFun" },
  { label: "百度", name: "百度" },
  { label: "B站", name: "哔哩哔哩" },
  { label: "酷安", name: "酷安" },
  { label: "CSDN", name: "CSDN" },
  { label: "数字尾巴", name: "数字尾巴" },
  { label: "豆瓣讨论", name: "豆瓣讨论" },
  { label: "豆瓣电影", name: "豆瓣电影" },
  { label: "抖音", name: "抖音" },
  { label: "极客公园", name: "极客公园" },
  { label: "原神", name: "原神" },
  { label: "果壳", name: "果壳" },
  { label: "HelloGitHub", name: "HelloGitHub" },
  { label: "历史上的今天", name: "历史上的今天" },
  { label: "崩坏3", name: "崩坏3" },
  { label: "虎扑", name: "虎扑" },
  { label: "虎嗅", name: "虎嗅" },
  { label: "爱范儿", name: "爱范儿" },
  { label: "IT之家「喜加一」", name: "IT之家「喜加一」" },
  { label: "IT之家", name: "IT之家" },
  { label: "简书", name: "简书" },
  { label: "掘金", name: "稀土掘金" },
  { label: "英雄联盟", name: "英雄联盟" },
  { label: "米游社·崩坏3", name: "米游社 · 崩坏3" },
  { label: "网易新闻", name: "网易新闻" },
  { label: "水木社区", name: "水木社区" },
  { label: "NGA", name: "NGA" },
  { label: "腾讯新闻", name: "腾讯新闻" },
  { label: "新浪新闻", name: "新浪新闻" },
  { label: "新浪网", name: "新浪网" },
  { label: "什么值得买", name: "什么值得买" },
  { label: "少数派", name: "少数派" },
  { label: "崩铁", name: "崩坏：星穹铁道" },
  { label: "澎湃新闻", name: "澎湃新闻" },
  { label: "贴吧", name: "百度贴吧" },
  { label: "头条", name: "今日头条" },
  { label: "中央气象台", name: "中央气象台" },
  { label: "微博", name: "微博" },
  { label: "微信读书", name: "微信读书" },
  { label: "游研社", name: "游研社" },
  { label: "知乎", name: "知乎" },
  { label: "知乎日报", name: "知乎日报" },
];

// 默认选中平台（有序）
const DEFAULT_SELECTED: string[] = [
  "稀土掘金", "百度", "哔哩哔哩", "吾爱破解",
  "抖音", "HelloGitHub", "果壳", "今日头条",
];

const STORAGE_KEY = "hot-tabs-settings";

// --- localStorage 持久化 ---
function loadSettings(): string[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const arr = JSON.parse(raw);
      if (Array.isArray(arr) && arr.length > 0) {
        // 过滤掉已不存在的平台
        const validNames = new Set(ALL_PLATFORMS.map((p) => p.name));
        const filtered = arr.filter((n: string) => validNames.has(n));
        if (filtered.length > 0) return filtered;
      }
    }
  } catch {
    // ignore
  }
  return [...DEFAULT_SELECTED];
}

function saveSettings(names: string[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(names));
}

// --- 当前选中的平台名列表（有序） ---
const selectedNames = ref<string[]>(loadSettings());

// 由 name 查找 platform 对象
function getPlatform(name: string): HotPlatform {
  return ALL_PLATFORMS.find((p) => p.name === name) || { label: name, name };
}

// 实际用于渲染 tabs 的列表
const tabsList = computed(() => selectedNames.value.map(getPlatform));

// 容器宽度
const containerWidth = computed(() => {
  return isMobile.value ? "290" : "420";
});

const activeName = ref(tabsList.value[0]?.name || "");

// 当 tabsList 变化（设置保存后），如果当前激活的 tab 不在列表中，切到第一个
watch(tabsList, (list) => {
  if (list.length && !list.some((t) => t.name === activeName.value)) {
    activeName.value = list[0].name;
  }
});

// --- 设置弹窗 ---
const showSettings = ref(false);
// 临时编辑列表（弹窗内操作，保存时才写入）
const editList = ref<string[]>([]);

function openSettings() {
  editList.value = [...selectedNames.value];
  showSettings.value = true;
}

function isChecked(name: string) {
  return editList.value.includes(name);
}

function togglePlatform(name: string) {
  const idx = editList.value.indexOf(name);
  if (idx !== -1) {
    editList.value.splice(idx, 1);
  } else {
    editList.value.push(name);
  }
}

function handleSaveSettings() {
  if (editList.value.length === 0) {
    return;
  }
  selectedNames.value = [...editList.value];
  saveSettings(selectedNames.value);
  showSettings.value = false;
}

function handleResetSettings() {
  editList.value = [...DEFAULT_SELECTED];
}

// 已选平台的 draggable 数据（computed proxy for editList mapped to objects）
const editSelectedPlatforms = computed(() =>
  editList.value.map(getPlatform),
);
</script>

<template>
  <el-popover
    placement="bottom-start"
    :width="containerWidth"
    :offset="5"
    trigger="hover"
  >
    <template #default>
      <div class="hot-content">
        <el-tabs v-model="activeName" class="hot-tabs">
          <m-hot-item
            :active-name="activeName"
            :name="tab.name"
            :label="tab.label"
            v-for="tab in tabsList"
            :key="tab.name"
          />
        </el-tabs>
        <div
          class="settings-btn"
          title="热榜设置"
          @click.stop="openSettings"
        >
          <m-icon icon="uil:setting" :size="14" />
        </div>
      </div>
    </template>
    <template #reference>
      <div class="flex items-center cursor-pointer">
        <m-icon icon="ph:fire-fill" color="#bb0c0c" />
        <span
          class="text-sm font-bold"
          :style="{ color }"
          >今日热榜</span
        >
      </div>
    </template>
  </el-popover>

  <!-- 设置弹窗 -->
  <el-dialog
    v-model="showSettings"
    title="热榜设置"
    :width="isMobile ? '95%' : '520px'"
    append-to-body
    destroy-on-close
  >
    <!-- 已选平台 - 可拖拽排序 -->
    <div class="settings-section">
      <div class="settings-label">已选平台（拖拽排序）</div>
      <VueDraggable
        v-model="editList"
        :animation="150"
        class="selected-tags"
      >
        <div
          v-for="name in editList"
          :key="name"
          class="selected-tag"
        >
          <m-icon icon="mdi:drag" :size="14" class="drag-icon" />
          <span>{{ getPlatform(name).label }}</span>
          <m-icon
            icon="ep:close"
            :size="12"
            class="remove-icon"
            @click="togglePlatform(name)"
          />
        </div>
      </VueDraggable>
      <div v-if="editList.length === 0" class="empty-tip">
        请至少选择一个平台
      </div>
    </div>

    <!-- 全部平台 - 复选 -->
    <div class="settings-section">
      <div class="settings-label">全部平台</div>
      <div class="platform-grid">
        <div
          v-for="p in ALL_PLATFORMS"
          :key="p.name"
          class="platform-item"
          :class="{ active: isChecked(p.name) }"
          @click="togglePlatform(p.name)"
        >
          {{ p.label }}
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-between">
        <el-button @click="handleResetSettings">恢复默认</el-button>
        <div>
          <el-button @click="showSettings = false">取消</el-button>
          <el-button type="primary" :disabled="editList.length === 0" @click="handleSaveSettings">保存</el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
.hot-content {
  position: relative;
}
.hot-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 0;
    // leave room for the settings icon on the right
    padding-right: 20px;
  }
}
.settings-btn {
  position: absolute;
  top: 6px;
  right: 0;
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
  color: var(--nav-text-secondary);
  z-index: 1;
  transition: color 0.2s;
  &:hover {
    color: var(--el-color-primary, #409eff);
  }
}

.settings-section {
  margin-bottom: 16px;
}
.settings-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--nav-text-secondary);
  margin-bottom: 8px;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  min-height: 32px;
  padding: 6px;
  border: 1px dashed var(--el-border-color, #dcdfe6);
  border-radius: 6px;
  background: var(--el-fill-color-lighter, #fafafa);
}
.selected-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: var(--el-color-primary-light-9, #ecf5ff);
  color: var(--el-color-primary, #409eff);
  border-radius: 4px;
  font-size: 12px;
  cursor: grab;
  user-select: none;
  &:active {
    cursor: grabbing;
  }
  .drag-icon {
    color: var(--el-color-primary-light-5, #a0cfff);
  }
  .remove-icon {
    cursor: pointer;
    color: var(--el-color-primary-light-5, #a0cfff);
    transition: color 0.15s;
    &:hover {
      color: #f56c6c;
    }
  }
}

.empty-tip {
  color: var(--nav-text-secondary);
  font-size: 12px;
  text-align: center;
  padding: 8px;
}

.platform-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.platform-item {
  padding: 5px 10px;
  border: 1px solid var(--el-border-color, #dcdfe6);
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  user-select: none;
  transition: all 0.15s;
  color: var(--nav-text);
  &:hover {
    border-color: var(--el-color-primary);
    color: var(--el-color-primary);
  }
  &.active {
    background: var(--el-color-primary);
    border-color: var(--el-color-primary);
    color: white;
  }
}
</style>
