<script setup lang="ts">
import { computed, ref } from 'vue';
import { NButton, NInput, NPopover, NScrollbar, NTabPane, NTabs, NUpload, type UploadFileInfo } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { fetchLinkSyncCdnFile } from '@/service/api';

defineOptions({ name: 'IconSelect' });

interface Props {
  /** Current icon value (iconify name or URL) */
  value?: string;
  /** Color for SVG icon preview */
  color?: string;
  /** Placeholder text */
  placeholder?: string;
  /** Whether to show upload button */
  showUpload?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  value: '',
  color: '',
  placeholder: 'iconify名称或图片URL',
  showUpload: true
});

const emit = defineEmits<{
  'update:value': [value: string];
}>();

const showPopover = ref(false);
const iconSearch = ref('');
const uploadLoading = ref(false);

// Icon presets with colorful icon sets
const iconCategories: Record<string, string[]> = {
  '彩色': [
    'flat-color-icons:home', 'flat-color-icons:settings', 'flat-color-icons:folder',
    'flat-color-icons:file', 'flat-color-icons:image-file', 'flat-color-icons:music',
    'flat-color-icons:video-file', 'flat-color-icons:search', 'flat-color-icons:link',
    'flat-color-icons:share', 'flat-color-icons:download', 'flat-color-icons:upload',
    'flat-color-icons:lock', 'flat-color-icons:key', 'flat-color-icons:clock',
    'flat-color-icons:calendar', 'flat-color-icons:like', 'flat-color-icons:bookmark',
    'flat-color-icons:globe', 'flat-color-icons:database', 'flat-color-icons:info',
    'flat-color-icons:idea', 'flat-color-icons:flash-on', 'flat-color-icons:services',
    'noto:star', 'noto:fire', 'noto:rocket', 'noto:package',
    'noto:eyes', 'noto:light-bulb', 'noto:laptop', 'noto:mobile-phone'
  ],
  '开发': [
    'logos:vue', 'logos:react', 'logos:angular-icon', 'logos:svelte-icon',
    'logos:javascript', 'logos:typescript-icon', 'logos:python', 'logos:java',
    'logos:go', 'logos:rust', 'logos:nodejs-icon', 'logos:deno',
    'logos:html-5', 'logos:css-3', 'logos:sass', 'logos:tailwindcss-icon',
    'logos:docker-icon', 'logos:kubernetes', 'logos:git-icon', 'logos:github-icon',
    'logos:gitlab', 'logos:visual-studio-code', 'logos:npm-icon', 'logos:yarn',
    'logos:postgresql', 'logos:mysql-icon', 'logos:redis', 'logos:mongodb-icon',
    'logos:linux-tux', 'logos:apple', 'logos:microsoft-icon', 'logos:android-icon'
  ],
  '社交': [
    'logos:google-icon', 'logos:youtube-icon', 'logos:twitter',
    'logos:facebook', 'logos:instagram-icon', 'logos:linkedin-icon',
    'logos:reddit-icon', 'logos:discord-icon', 'logos:telegram',
    'logos:whatsapp-icon', 'logos:slack-icon', 'logos:skype',
    'logos:twitch', 'logos:spotify-icon', 'logos:steam-icon',
    'flat-color-icons:video-call', 'flat-color-icons:phone',
    'flat-color-icons:feedback', 'flat-color-icons:faq',
    'flat-color-icons:comments', 'flat-color-icons:collaboration',
    'noto:speech-balloon', 'noto:love-letter', 'noto:handshake', 'noto:waving-hand'
  ],
  '通用': [
    'mdi:home', 'mdi:cog', 'mdi:account', 'mdi:star', 'mdi:heart', 'mdi:bookmark',
    'mdi:folder', 'mdi:file', 'mdi:image', 'mdi:video', 'mdi:music', 'mdi:email',
    'mdi:phone', 'mdi:map-marker', 'mdi:clock', 'mdi:calendar', 'mdi:bell',
    'mdi:search', 'mdi:link', 'mdi:share', 'mdi:download', 'mdi:upload',
    'mdi:cloud', 'mdi:lock', 'mdi:key', 'mdi:shield', 'mdi:check', 'mdi:close',
    'mdi:plus', 'mdi:minus', 'mdi:pencil', 'mdi:delete', 'mdi:refresh', 'mdi:eye'
  ],
  '导航': [
    'pajamas:link', 'ep:menu', 'ic:round-menu', 'mdi:view-dashboard', 'mdi:chart-bar',
    'mdi:chart-line', 'mdi:chart-pie', 'mdi:table', 'mdi:format-list-bulleted',
    'mdi:apps', 'mdi:view-grid', 'mdi:view-list', 'mdi:sitemap',
    'fluent-mdl2:message-friend-request', 'icon-park-outline:system',
    'dashicons:admin-site', 'mdi:web', 'mdi:earth',
    'mdi:github', 'mdi:code-tags', 'mdi:console', 'mdi:database',
    'mdi:server', 'mdi:api', 'mdi:bug', 'mdi:rocket', 'mdi:cube'
  ]
};

const filteredIcons = computed(() => {
  if (!iconSearch.value) return iconCategories;
  const keyword = iconSearch.value.toLowerCase();
  const result: Record<string, string[]> = {};
  for (const [cat, icons] of Object.entries(iconCategories)) {
    const matched = icons.filter(icon => icon.toLowerCase().includes(keyword));
    if (matched.length) result[cat] = matched;
  }
  return result;
});

function selectIcon(icon: string) {
  emit('update:value', icon);
  showPopover.value = false;
}

function handleInputUpdate(val: string) {
  emit('update:value', val);
}

// Icon preview logic
const isUrl = computed(() => props.value?.startsWith('http'));
const isIconify = computed(() => props.value && !isUrl.value);

// Upload handler
async function handleUpload({ file }: { file: UploadFileInfo }) {
  if (!file.file) return;
  uploadLoading.value = true;
  try {
    const { data, error } = await fetchLinkSyncCdnFile(file.file);
    if (!error && data) {
      const cdnUrl = typeof data === 'string' ? data : (data as any).url || (data as any).icon || '';
      if (cdnUrl) {
        emit('update:value', cdnUrl);
        window.$message?.success('上传成功');
      }
    }
  } finally {
    uploadLoading.value = false;
  }
}
</script>

<template>
  <div class="flex items-center gap-8px w-full">
    <NInput class="flex-1" :value="value" :placeholder="placeholder" @update:value="handleInputUpdate" />
    <NPopover v-model:show="showPopover" trigger="click" placement="bottom-end" :width="420">
      <template #trigger>
        <NButton type="primary" ghost class="flex-shrink-0">选择图标</NButton>
      </template>
      <div class="p-4px">
        <NInput v-model:value="iconSearch" placeholder="搜索图标..." clearable size="small" class="mb-8px" />
        <NScrollbar style="max-height: 300px">
          <NTabs type="segment" size="small">
            <NTabPane v-for="(icons, category) in filteredIcons" :key="category" :name="category" :tab="category">
              <div class="grid grid-cols-8 gap-4px mt-8px">
                <div
                  v-for="icon in icons"
                  :key="icon"
                  class="flex-center p-6px cursor-pointer rounded hover:bg-primary/10 transition-colors"
                  :title="icon"
                  @click="selectIcon(icon)"
                >
                  <Icon :icon="icon" class="text-22px" />
                </div>
              </div>
            </NTabPane>
          </NTabs>
        </NScrollbar>
      </div>
    </NPopover>
    <NUpload
      v-if="showUpload"
      :show-file-list="false"
      accept="image/*,.svg"
      :custom-request="({ file }) => handleUpload({ file: file as UploadFileInfo })"
      class="flex-shrink-0"
      style="width: auto"
    >
      <NButton type="default" :loading="uploadLoading" title="上传图标">
        <template #icon>
          <Icon icon="mdi:upload" />
        </template>
      </NButton>
    </NUpload>
    <!-- Preview -->
    <div
      v-if="value"
      class="flex-center w-36px h-36px rounded border border-gray-200 dark:border-gray-600 flex-shrink-0"
    >
      <img v-if="isUrl" :src="value" class="w-28px h-28px rounded object-contain" />
      <Icon v-else-if="isIconify" :icon="value" class="text-24px" :color="color || undefined" />
    </div>
  </div>
</template>
