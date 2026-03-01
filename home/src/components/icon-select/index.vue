<script setup lang="ts">
import { computed, ref } from "vue";
import MIcon from "@/components/MIcon.vue";

defineOptions({ name: "MIconSelect" });

const props = withDefaults(
  defineProps<{
    modelValue?: string;
    color?: string;
    placeholder?: string;
  }>(),
  {
    modelValue: "",
    color: "",
    placeholder: "iconify名称或图片URL",
  },
);

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const popoverVisible = ref(false);
const iconSearch = ref("");

const iconCategories: Record<string, string[]> = {
  彩色: [
    "flat-color-icons:home", "flat-color-icons:settings", "flat-color-icons:folder",
    "flat-color-icons:file", "flat-color-icons:image-file", "flat-color-icons:music",
    "flat-color-icons:video-file", "flat-color-icons:search", "flat-color-icons:link",
    "flat-color-icons:share", "flat-color-icons:download", "flat-color-icons:upload",
    "flat-color-icons:lock", "flat-color-icons:key", "flat-color-icons:clock",
    "flat-color-icons:calendar", "flat-color-icons:like", "flat-color-icons:bookmark",
    "flat-color-icons:globe", "flat-color-icons:database", "flat-color-icons:info",
    "flat-color-icons:idea", "flat-color-icons:flash-on", "flat-color-icons:services",
    "noto:star", "noto:fire", "noto:rocket", "noto:package",
    "noto:eyes", "noto:light-bulb", "noto:laptop", "noto:mobile-phone",
  ],
  开发: [
    "logos:vue", "logos:react", "logos:angular-icon", "logos:svelte-icon",
    "logos:javascript", "logos:typescript-icon", "logos:python", "logos:java",
    "logos:go", "logos:rust", "logos:nodejs-icon", "logos:deno",
    "logos:html-5", "logos:css-3", "logos:sass", "logos:tailwindcss-icon",
    "logos:docker-icon", "logos:kubernetes", "logos:git-icon", "logos:github-icon",
    "logos:gitlab", "logos:visual-studio-code", "logos:npm-icon", "logos:yarn",
    "logos:postgresql", "logos:mysql-icon", "logos:redis", "logos:mongodb-icon",
    "logos:linux-tux", "logos:apple", "logos:microsoft-icon", "logos:android-icon",
  ],
  社交: [
    "logos:google-icon", "logos:youtube-icon", "logos:twitter",
    "logos:facebook", "logos:instagram-icon", "logos:linkedin-icon",
    "logos:reddit-icon", "logos:discord-icon", "logos:telegram",
    "logos:whatsapp-icon", "logos:slack-icon", "logos:skype",
    "logos:twitch", "logos:spotify-icon", "logos:steam-icon",
    "flat-color-icons:video-call", "flat-color-icons:phone",
    "flat-color-icons:feedback", "flat-color-icons:faq",
    "flat-color-icons:comments", "flat-color-icons:collaboration",
    "noto:speech-balloon", "noto:love-letter", "noto:handshake", "noto:waving-hand",
  ],
  通用: [
    "mdi:home", "mdi:cog", "mdi:account", "mdi:star", "mdi:heart", "mdi:bookmark",
    "mdi:folder", "mdi:file", "mdi:image", "mdi:video", "mdi:music", "mdi:email",
    "mdi:phone", "mdi:map-marker", "mdi:clock", "mdi:calendar", "mdi:bell",
    "mdi:search", "mdi:link", "mdi:share", "mdi:download", "mdi:upload",
    "mdi:cloud", "mdi:lock", "mdi:key", "mdi:shield", "mdi:check", "mdi:close",
    "mdi:plus", "mdi:minus", "mdi:pencil", "mdi:delete", "mdi:refresh", "mdi:eye",
  ],
  导航: [
    "pajamas:link", "ep:menu", "ic:round-menu", "mdi:view-dashboard", "mdi:chart-bar",
    "mdi:chart-line", "mdi:chart-pie", "mdi:table", "mdi:format-list-bulleted",
    "mdi:apps", "mdi:view-grid", "mdi:view-list", "mdi:sitemap",
    "fluent-mdl2:message-friend-request", "icon-park-outline:system",
    "dashicons:admin-site", "mdi:web", "mdi:earth",
    "mdi:github", "mdi:code-tags", "mdi:console", "mdi:database",
    "mdi:server", "mdi:api", "mdi:bug", "mdi:rocket", "mdi:cube",
  ],
};

const filteredIcons = computed(() => {
  if (!iconSearch.value) return iconCategories;
  const keyword = iconSearch.value.toLowerCase();
  const result: Record<string, string[]> = {};
  for (const [cat, icons] of Object.entries(iconCategories)) {
    const matched = icons.filter((icon) => icon.toLowerCase().includes(keyword));
    if (matched.length) result[cat] = matched;
  }
  return result;
});

const isUrl = computed(() => props.modelValue?.startsWith("http"));

function selectIcon(icon: string) {
  emit("update:modelValue", icon);
  popoverVisible.value = false;
}

function handleInput(val: string) {
  emit("update:modelValue", val);
}
</script>

<template>
  <div class="icon-select">
    <el-input
      :model-value="modelValue"
      :placeholder="placeholder"
      @update:model-value="handleInput"
      class="icon-select-input"
    >
      <template #append>
        <div class="icon-preview" v-if="modelValue">
          <img v-if="isUrl" :src="modelValue" class="preview-img" />
          <m-icon v-else :icon="modelValue" :color="color" :size="22" />
        </div>
      </template>
    </el-input>
    <el-popover
      v-model:visible="popoverVisible"
      trigger="click"
      placement="bottom-end"
      :width="400"
    >
      <template #reference>
        <el-button type="primary" plain class="icon-select-btn">选择图标</el-button>
      </template>
      <div>
        <el-input
          v-model="iconSearch"
          placeholder="搜索图标..."
          clearable
          size="small"
          class="mb-2"
        />
        <el-scrollbar height="280px">
          <el-tabs type="border-card" size="small">
            <el-tab-pane
              v-for="(icons, category) in filteredIcons"
              :key="category"
              :label="String(category)"
            >
              <div class="icon-grid">
                <div
                  v-for="icon in icons"
                  :key="icon"
                  class="icon-grid-item"
                  :title="icon"
                  @click="selectIcon(icon)"
                >
                  <m-icon :icon="icon" :size="22" />
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-scrollbar>
      </div>
    </el-popover>
  </div>
</template>

<style lang="scss" scoped>
.icon-select {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.icon-select-input {
  flex: 1;
}

.icon-select-btn {
  flex-shrink: 0;
}

.icon-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
}

.preview-img {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  object-fit: contain;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 4px;
  padding: 4px 0;
}

.icon-grid-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.15s;

  &:hover {
    background-color: var(--el-color-primary-light-9);
  }
}
</style>
