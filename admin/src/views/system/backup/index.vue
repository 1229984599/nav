<script setup lang="ts">
import { ref } from 'vue';
import { NButton, NCard, NPopconfirm, NProgress, NSpace } from 'naive-ui';
import { Icon } from '@iconify/vue';
import {
  fetchSiteBackup, fetchSiteBackupList, fetchSiteBackupDelete,
  fetchSiteRestore, fetchSiteRestoreUpload
} from '@/service/api';
import { getServiceBaseURL } from '@/utils/service';
import { getAuthorization } from '@/service/request/shared';
import { createTaskWebSocket } from '@/utils/websocket';

const backupLoading = ref(false);
const backupProgress = ref<{ message: string; current: number; total: number } | null>(null);
const restoreLoading = ref(false);
const restoreProgress = ref<{ message: string; current: number; total: number } | null>(null);
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
  backupProgress.value = null;
  const { data, error } = await fetchSiteBackup();

  if (error || !data?.task_id) {
    backupLoading.value = false;
    return;
  }

  createTaskWebSocket(
    data.task_id,
    (result) => {
      backupLoading.value = false;
      backupProgress.value = null;
      window.$message?.success(`备份成功：${result.filename}`);
      loadBackupList();
    },
    (errMsg) => {
      backupLoading.value = false;
      backupProgress.value = null;
      window.$message?.error(errMsg || '备份失败');
    },
    (progress) => {
      backupProgress.value = progress;
    }
  );
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

function _startRestoreWs(taskId: string) {
  createTaskWebSocket(
    taskId,
    () => {
      restoreLoading.value = false;
      restoreProgress.value = null;
      window.$message?.success('数据恢复成功');
      loadBackupList();
    },
    (errMsg) => {
      restoreLoading.value = false;
      restoreProgress.value = null;
      window.$message?.error(errMsg || '数据恢复失败');
    },
    (progress) => {
      restoreProgress.value = progress;
    }
  );
}

async function handleRestoreFromServer(filename: string) {
  restoreLoading.value = true;
  restoreProgress.value = null;
  const { data, error } = await fetchSiteRestore(filename);

  if (error || !data?.task_id) {
    restoreLoading.value = false;
    return;
  }

  _startRestoreWs(data.task_id);
}

const restoreFileRef = ref<HTMLInputElement | null>(null);
function handleRestoreUploadClick() {
  restoreFileRef.value?.click();
}
async function handleRestoreFile(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  restoreLoading.value = true;
  restoreProgress.value = null;
  const { data, error } = await fetchSiteRestoreUpload(file);

  if (restoreFileRef.value) restoreFileRef.value.value = '';

  if (error || !data?.task_id) {
    restoreLoading.value = false;
    return;
  }

  _startRestoreWs(data.task_id);
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

loadBackupList();
</script>

<template>
  <div class="overflow-auto p-16px">
    <div class="max-w-900px mx-auto flex flex-col gap-16px">
      <div class="flex items-center justify-between">
        <h2 class="text-20px font-bold m-0">备份管理</h2>
        <NSpace>
          <NButton :loading="restoreLoading" @click="handleRestoreUploadClick">
            <template #icon><Icon icon="mdi:database-import" /></template>
            从文件恢复
          </NButton>
          <NButton type="primary" :loading="backupLoading" @click="handleBackup">
            <template #icon><Icon icon="mdi:database-export" /></template>
            创建备份
          </NButton>
          <input ref="restoreFileRef" type="file" accept=".json" style="display:none" @change="handleRestoreFile">
        </NSpace>
      </div>

      <!-- Backup progress -->
      <div v-if="backupProgress" class="flex items-center gap-12px">
        <NProgress
          type="line"
          :percentage="Math.round((backupProgress.current / backupProgress.total) * 100)"
          indicator-placement="inside"
          :height="20"
          :border-radius="4"
          processing
          class="flex-1"
        />
        <span class="text-12px text-gray-400 flex-shrink-0 whitespace-nowrap">
          {{ backupProgress.message }}
        </span>
      </div>
      <!-- Restore progress -->
      <div v-if="restoreProgress" class="flex items-center gap-12px">
        <NProgress
          type="line"
          :percentage="Math.round((restoreProgress.current / restoreProgress.total) * 100)"
          indicator-placement="inside"
          :height="20"
          :border-radius="4"
          processing
          class="flex-1"
        />
        <span class="text-12px text-gray-400 flex-shrink-0 whitespace-nowrap">
          {{ restoreProgress.message }}
        </span>
      </div>

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
                <NButton size="small" type="info" :disabled="restoreLoading">恢复</NButton>
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
      <div v-else class="text-14px text-gray-400 py-8px text-center">暂无备份文件</div>
    </div>
  </div>
</template>
