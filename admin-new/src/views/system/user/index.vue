<script setup lang="ts">
import { computed, h, reactive, ref } from 'vue';
import { NButton, NDataTable, NForm, NFormItem, NInput, NModal, NPagination, NPopconfirm, NSelect, NSpace, NSwitch, NTag, type DataTableColumns } from 'naive-ui';
import { fetchUserList, fetchUserCreate, fetchUserUpdate, fetchUserDelete } from '@/service/api';

const loading = ref(false);
const tableData = ref<Api.SystemUser.UserItem[]>([]);
const pagination = reactive({ page: 1, pageSize: 20, total: 0 });
const checkedRowKeys = ref<number[]>([]);

const filters = reactive<Api.SystemUser.UserFilter>({ username: '', status: null });
const showDialog = ref(false);
const isEdit = ref(false);
const editId = ref<number | null>(null);

const formModel = reactive({
  username: '',
  password: '',
  nickname: '',
  status: false as boolean
});

const statusOptions = [
  { label: '全部', value: null },
  { label: '启用', value: true },
  { label: '禁用', value: false }
];

async function loadData() {
  loading.value = true;
  const filterData: any = {};
  if (filters.username) filterData.username = filters.username;
  if (filters.status !== null && filters.status !== undefined) filterData.status = filters.status;

  const { data, error } = await fetchUserList(
    { page: pagination.page, size: pagination.pageSize },
    filterData
  );
  if (!error && data) {
    tableData.value = data.items;
    pagination.total = data.total;
  }
  loading.value = false;
}

function handleSearch() { pagination.page = 1; loadData(); }
function handleReset() { filters.username = ''; filters.status = null; handleSearch(); }
function handlePageChange(page: number) { pagination.page = page; loadData(); }
function handlePageSizeChange(size: number) { pagination.pageSize = size; pagination.page = 1; loadData(); }

function handleAdd() {
  isEdit.value = false;
  editId.value = null;
  Object.assign(formModel, { username: '', password: '', nickname: '', status: false });
  showDialog.value = true;
}

function handleEdit(row: Api.SystemUser.UserItem) {
  isEdit.value = true;
  editId.value = row.id;
  Object.assign(formModel, {
    username: row.username,
    password: '',
    nickname: row.nickname || '',
    status: row.status
  });
  showDialog.value = true;
}

async function handleSave() {
  if (isEdit.value && editId.value) {
    const payload: Api.SystemUser.UserUpdate = {
      nickname: formModel.nickname,
      status: formModel.status
    };
    if (formModel.password) payload.password = formModel.password;
    await fetchUserUpdate(editId.value, payload);
  } else {
    await fetchUserCreate({
      username: formModel.username,
      password: formModel.password,
      nickname: formModel.nickname,
      status: formModel.status
    });
  }
  showDialog.value = false;
  loadData();
}

async function handleDelete(ids: string) { await fetchUserDelete(ids); loadData(); }

async function handleBatchDelete() {
  if (!checkedRowKeys.value.length) return;
  await fetchUserDelete(checkedRowKeys.value.join(','));
  checkedRowKeys.value = [];
  loadData();
}

const columns = computed<DataTableColumns<Api.SystemUser.UserItem>>(() => [
  { type: 'selection' },
  { title: 'ID', key: 'id', width: 60 },
  { title: '用户名', key: 'username', width: 150 },
  { title: '昵称', key: 'nickname', width: 150 },
  {
    title: '状态', key: 'status', width: 80,
    render(row) {
      return h(NTag, { type: row.status ? 'success' : 'error', size: 'small' }, () => row.status ? '启用' : '禁用');
    }
  },
  {
    title: '超级管理员', key: 'is_super', width: 100,
    render(row) {
      return h(NTag, { type: row.is_super ? 'warning' : 'default', size: 'small' }, () => row.is_super ? '是' : '否');
    }
  },
  {
    title: '操作', key: 'actions', width: 150,
    render(row) {
      return h(NSpace, { size: 8 }, () => [
        h(NButton, { size: 'small', type: 'primary', onClick: () => handleEdit(row) }, () => '编辑'),
        h(NPopconfirm, { onPositiveClick: () => handleDelete(String(row.id)) }, {
          trigger: () => h(NButton, { size: 'small', type: 'error' }, () => '删除'),
          default: () => '确定删除？'
        })
      ]);
    }
  }
]);

loadData();
</script>

<template>
  <div class="flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <NForm inline label-placement="left" class="gap-12px">
      <NFormItem label="用户名">
        <NInput v-model:value="filters.username" placeholder="用户名" clearable @keyup.enter="handleSearch" />
      </NFormItem>
      <NFormItem label="状态">
        <NSelect v-model:value="filters.status" :options="statusOptions" style="width: 100px" />
      </NFormItem>
      <NFormItem>
        <NSpace>
          <NButton type="primary" @click="handleSearch">搜索</NButton>
          <NButton @click="handleReset">重置</NButton>
        </NSpace>
      </NFormItem>
    </NForm>

    <NSpace class="mb-12px">
      <NButton type="primary" @click="handleAdd">新增</NButton>
      <NPopconfirm @positive-click="handleBatchDelete">
        <template #trigger>
          <NButton type="error" :disabled="!checkedRowKeys.length">批量删除</NButton>
        </template>
        确定删除选中的 {{ checkedRowKeys.length }} 项？
      </NPopconfirm>
    </NSpace>

    <NDataTable
      v-model:checked-row-keys="checkedRowKeys"
      :columns="columns"
      :data="tableData"
      :loading="loading"
      :row-key="(row: Api.SystemUser.UserItem) => row.id"
      :scroll-x="700"
      flex-height
      class="flex-1-hidden"
    />

    <div class="flex justify-end mt-12px">
      <NPagination
        v-model:page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :item-count="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        show-size-picker
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </div>

    <NModal v-model:show="showDialog" preset="dialog" :title="isEdit ? '编辑用户' : '新增用户'" style="width: 450px">
      <NForm label-placement="left" label-width="80px" class="mt-16px">
        <NFormItem label="用户名">
          <NInput v-model:value="formModel.username" :disabled="isEdit" placeholder="用户名" />
        </NFormItem>
        <NFormItem label="密码">
          <NInput v-model:value="formModel.password" type="password" show-password-on="click"
            :placeholder="isEdit ? '留空则不修改' : '密码'" />
        </NFormItem>
        <NFormItem label="昵称">
          <NInput v-model:value="formModel.nickname" placeholder="昵称" />
        </NFormItem>
        <NFormItem label="状态">
          <NSwitch v-model:value="formModel.status" />
        </NFormItem>
      </NForm>
      <template #action>
        <NButton @click="showDialog = false">取消</NButton>
        <NButton type="primary" @click="handleSave">保存</NButton>
      </template>
    </NModal>
  </div>
</template>
