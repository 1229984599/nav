<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { NButton, NCard, NColorPicker, NForm, NFormItem, NInput, NPopconfirm, NSpace, NSwitch, NTag } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { fetchSiteGet, fetchSiteUpdate, fetchSiteClearCache, fetchSiteBackup, fetchSiteBackupList, fetchSiteBackupDelete, fetchSiteRestore, fetchSiteRestoreUpload } from '@/service/api';
import { getServiceBaseURL } from '@/utils/service';
import { getAuthorization } from '@/service/request/shared';

const loading = ref(false);
const saving = ref(false);
const formModel = reactive<Api.Site.SiteUpdate>({
  title: '',
  desc: '',
  keywords: '',
  icon: '',
  color: '',
  footer: '',
  yiyan: false,
  weather: false,
  weather_key: '',
  copyright: '',
  cdn_img_token: ''
});

async function loadData() {
  loading.value = true;
  const { data, error } = await fetchSiteGet();
  if (!error && data) {
    Object.assign(formModel, {
      id: data.id,
      title: data.title || '',
      desc: data.desc || '',
      keywords: data.keywords || '',
      icon: data.icon || '',
      color: data.color || '',
      footer: data.footer || '',
      yiyan: data.yiyan,
      weather: data.weather,
      weather_key: data.weather_key || '',
      copyright: data.copyright || '',
      cdn_img_token: data.cdn_img_token || ''
    });
  }
  loading.value = false;
}

async function handleSave() {
  saving.value = true;
  const { error } = await fetchSiteUpdate(formModel);
  if (!error) {
    window.$message?.success('保存成功');
  }
  saving.value = false;
}

async function handleClearCache() {
  const { error } = await fetchSiteClearCache();
  if (!error) {
    window.$message?.success('缓存已清除');
  }
}

// Backup / Restore
const backupLoading = ref(false);
const backupList = ref<Array<{ filename: string; size: number; created_at: string }>>([]);
const isHttpProxy = import.meta.env.DEV && import.meta.env.VITE_HTTP_PROXY === 'Y';
const { baseURL } = getServiceBaseURL(import.meta.env, isHttpProxy);

async function loadBackupList() {
  const { data, error } = await fetchSiteBackupList();
  if (!error && data) {
    backupList.value = data;
  }
}

async function handleBackup() {
  backupLoading.value = true;
  const { data, error } = await fetchSiteBackup();
  backupLoading.value = false;
  if (!error && data) {
    window.$message?.success(`备份成功：${data.filename}`);
    loadBackupList();
  }
}

function handleDownloadBackup(filename: string) {
  const token = getAuthorization();
  const url = `${baseURL}/site/backup/download/${filename}`;
  fetch(url, { headers: { Authorization: token } })
    .then(res => res.blob())
    .then(blob => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      a.click();
      URL.revokeObjectURL(a.href);
    });
}

async function handleDeleteBackup(filename: string) {
  const { error } = await fetchSiteBackupDelete(filename);
  if (!error) {
    window.$message?.success('备份已删除');
    loadBackupList();
  }
}

async function handleRestoreFromServer(filename: string) {
  const { error } = await fetchSiteRestore(filename);
  if (!error) {
    window.$message?.success('数据恢复成功');
    loadData();
  }
}

const restoreFileRef = ref<HTMLInputElement | null>(null);
function handleRestoreUploadClick() {
  restoreFileRef.value?.click();
}
async function handleRestoreFile(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  const { error } = await fetchSiteRestoreUpload(file);
  if (!error) {
    window.$message?.success('数据恢复成功');
    loadData();
  }
  if (restoreFileRef.value) restoreFileRef.value.value = '';
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

loadData();
loadBackupList();
</script>

<template>
  <div class="overflow-auto p-16px">
    <div class="max-w-900px mx-auto flex flex-col gap-16px">
      <!-- Header with save/cache buttons -->
      <div class="flex items-center justify-between">
        <h2 class="text-20px font-bold m-0">站点设置</h2>
        <NSpace>
          <NButton type="warning" @click="handleClearCache">
            <template #icon><Icon icon="mdi:cached" /></template>
            清除缓存
          </NButton>
          <NButton type="primary" :loading="saving" @click="handleSave">
            <template #icon><Icon icon="mdi:content-save" /></template>
            保存设置
          </NButton>
        </NSpace>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16px">
        <!-- Basic Info Card -->
        <NCard class="lg:col-span-2">
          <template #header>
            <div class="flex items-center gap-8px">
              <Icon icon="mdi:web" class="text-18px text-primary" />
              <span>基本信息</span>
            </div>
          </template>
          <NForm label-placement="left" label-width="100px" :model="formModel">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-24px">
              <NFormItem label="站点标题">
                <NInput v-model:value="formModel.title" placeholder="输入站点标题" />
              </NFormItem>
              <NFormItem label="关键词">
                <NInput v-model:value="formModel.keywords" placeholder="SEO 关键词，用逗号分隔" />
              </NFormItem>
            </div>
            <NFormItem label="站点描述">
              <NInput v-model:value="formModel.desc" type="textarea" placeholder="站点描述，用于 SEO" :autosize="{ minRows: 2, maxRows: 4 }" />
            </NFormItem>
          </NForm>
        </NCard>

        <!-- Appearance Card -->
        <NCard>
          <template #header>
            <div class="flex items-center gap-8px">
              <Icon icon="mdi:palette" class="text-18px text-primary" />
              <span>外观设置</span>
            </div>
          </template>
          <NForm label-placement="left" label-width="80px" :model="formModel">
            <NFormItem label="站点图标">
              <IconSelect v-model:value="formModel.icon" placeholder="iconify名称或图片URL" />
            </NFormItem>
            <NFormItem label="主题色">
              <NColorPicker v-model:value="formModel.color" :modes="['hex']" :show-alpha="false" />
            </NFormItem>
          </NForm>
        </NCard>

        <!-- Feature Switches Card -->
        <NCard>
          <template #header>
            <div class="flex items-center gap-8px">
              <Icon icon="mdi:toggle-switch" class="text-18px text-primary" />
              <span>功能开关</span>
            </div>
          </template>
          <NForm label-placement="left" label-width="80px" :model="formModel">
            <NFormItem label="一言">
              <div class="flex items-center gap-12px w-full">
                <NSwitch v-model:value="formModel.yiyan" />
                <span class="text-12px text-gray-400">首页展示随机一言</span>
              </div>
            </NFormItem>
            <NFormItem label="天气">
              <div class="flex items-center gap-12px w-full">
                <NSwitch v-model:value="formModel.weather" />
                <span class="text-12px text-gray-400">首页展示天气信息</span>
              </div>
            </NFormItem>
            <NFormItem v-if="formModel.weather" label="天气 Key">
              <NInput v-model:value="formModel.weather_key" placeholder="和风天气 API Key" type="password" show-password-on="click" />
            </NFormItem>
          </NForm>
        </NCard>

        <!-- Integration Card -->
        <NCard class="lg:col-span-2">
          <template #header>
            <div class="flex items-center gap-8px">
              <Icon icon="mdi:puzzle" class="text-18px text-primary" />
              <span>集成配置</span>
            </div>
          </template>
          <NForm label-placement="left" label-width="120px" :model="formModel">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-24px">
              <NFormItem label="CDN图床Token">
                <NInput v-model:value="formModel.cdn_img_token" placeholder="图床 Token" type="password" show-password-on="click" />
              </NFormItem>
              <NFormItem label="版权/备案号">
                <NInput v-model:value="formModel.copyright" placeholder="如：京ICP备xxxxxxxx号" />
              </NFormItem>
            </div>
            <NFormItem label="底部文字">
              <NInput v-model:value="formModel.footer" type="textarea" placeholder="页脚自定义文字，支持 HTML" :autosize="{ minRows: 2, maxRows: 4 }" />
            </NFormItem>
          </NForm>
        </NCard>

        <!-- Backup & Restore Card -->
        <NCard class="lg:col-span-2">
          <template #header>
            <div class="flex items-center gap-8px">
              <Icon icon="mdi:backup-restore" class="text-18px text-primary" />
              <span>数据备份与恢复</span>
            </div>
          </template>
          <div class="flex flex-col gap-16px">
            <NSpace>
              <NButton type="primary" :loading="backupLoading" @click="handleBackup">
                <template #icon><Icon icon="mdi:database-export" /></template>
                创建备份
              </NButton>
              <NButton @click="handleRestoreUploadClick">
                <template #icon><Icon icon="mdi:database-import" /></template>
                从文件恢复
              </NButton>
              <input ref="restoreFileRef" type="file" accept=".json" style="display:none" @change="handleRestoreFile">
            </NSpace>
            <div v-if="backupList.length" class="flex flex-col gap-8px">
              <div
                v-for="item in backupList"
                :key="item.filename"
                class="flex items-center justify-between p-12px rounded-8px bg-gray-50 dark:bg-gray-800"
              >
                <div class="flex items-center gap-12px">
                  <Icon icon="mdi:file-document" class="text-20px text-gray-400" />
                  <div>
                    <div class="text-14px">{{ item.filename }}</div>
                    <div class="text-12px text-gray-400">{{ item.created_at }} · {{ formatSize(item.size) }}</div>
                  </div>
                </div>
                <NSpace :size="4">
                  <NButton size="small" @click="handleDownloadBackup(item.filename)">下载</NButton>
                  <NPopconfirm @positive-click="handleRestoreFromServer(item.filename)">
                    <template #trigger>
                      <NButton size="small" type="info">恢复</NButton>
                    </template>
                    确定从此备份恢复所有数据？当前数据将被覆盖！
                  </NPopconfirm>
                  <NPopconfirm @positive-click="handleDeleteBackup(item.filename)">
                    <template #trigger>
                      <NButton size="small" type="error">删除</NButton>
                    </template>
                    确定删除此备份？
                  </NPopconfirm>
                </NSpace>
              </div>
            </div>
            <div v-else class="text-14px text-gray-400 py-8px">暂无备份文件</div>
          </div>
        </NCard>
      </div>
    </div>
  </div>
</template>
