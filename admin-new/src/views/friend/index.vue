<script setup lang="ts">
import { computed, h, reactive, ref } from 'vue';
import { NButton, NColorPicker, NDataTable, NForm, NFormItem, NInput, NInputGroup, NInputNumber, NModal, NPagination, NPopconfirm, NSelect, NSpace, NSwitch, NTag, type DataTableColumns } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { fetchFriendList, fetchFriendCreate, fetchFriendUpdate, fetchFriendDelete, fetchFriendSiteInfo } from '@/service/api';

const loading = ref(false);
const tableData = ref<Api.Friend.FriendItem[]>([]);
const pagination = reactive({ page: 1, pageSize: 20, total: 0 });
const checkedRowKeys = ref<number[]>([]);

const filters = reactive<Api.Friend.FriendFilter>({ title: '', status: null });
const showDialog = ref(false);
const isEdit = ref(false);
const editId = ref<number | null>(null);
const formModel = reactive<Api.Friend.FriendCreate>({
  title: '', href: '', icon: '', desc: '', color: '', order: 0, status: true
});

const statusOptions = [
  { label: '全部', value: null },
  { label: '启用', value: true },
  { label: '禁用', value: false }
];

async function loadData() {
  loading.value = true;
  const filterData: any = {};
  if (filters.title) filterData.title = filters.title;
  if (filters.status !== null && filters.status !== undefined) filterData.status = filters.status;

  const { data, error } = await fetchFriendList(
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
function handleReset() { filters.title = ''; filters.status = null; handleSearch(); }
function handlePageChange(page: number) { pagination.page = page; loadData(); }
function handlePageSizeChange(size: number) { pagination.pageSize = size; pagination.page = 1; loadData(); }

function handleAdd() {
  isEdit.value = false;
  editId.value = null;
  Object.assign(formModel, { title: '', href: '', icon: '', desc: '', color: '', order: 0, status: true });
  showDialog.value = true;
}

function handleEdit(row: Api.Friend.FriendItem) {
  isEdit.value = true;
  editId.value = row.id;
  Object.assign(formModel, {
    title: row.title, href: row.href, icon: row.icon || '',
    desc: row.desc || '', color: row.color || '', order: row.order || 0, status: row.status
  });
  showDialog.value = true;
}

async function handleSave() {
  if (isEdit.value && editId.value) {
    await fetchFriendUpdate(editId.value, formModel);
  } else {
    await fetchFriendCreate(formModel);
  }
  showDialog.value = false;
  loadData();
}

async function handleDelete(ids: string) { await fetchFriendDelete(ids); loadData(); }

async function handleBatchDelete() {
  if (!checkedRowKeys.value.length) return;
  await fetchFriendDelete(checkedRowKeys.value.join(','));
  checkedRowKeys.value = [];
  loadData();
}

// Spider in form
const spiderLoading = ref(false);
async function handleFormSpider() {
  if (!formModel.href) {
    window.$message?.warning('请先输入链接地址');
    return;
  }
  spiderLoading.value = true;
  const { data, error } = await fetchFriendSiteInfo(formModel.href);
  if (!error && data) {
    if (data.title) formModel.title = data.title;
    if (data.icon) formModel.icon = data.icon;
    if (data.desc) formModel.desc = data.desc;
    window.$message?.success('抓取成功');
  }
  spiderLoading.value = false;
}

const columns = computed<DataTableColumns<Api.Friend.FriendItem>>(() => [
  { type: 'selection' },
  { title: 'ID', key: 'id', width: 60 },
  { title: '标题', key: 'title', width: 150, ellipsis: { tooltip: true } },
  { title: '链接', key: 'href', width: 200, ellipsis: { tooltip: true } },
  {
    title: '图标', key: 'icon', width: 60,
    render(row) {
      if (!row.icon) return '';
      const wrapper = (child: any) =>
        h('div', { style: 'display:flex;align-items:center;justify-content:center;width:28px;height:28px;' }, child);
      if (row.icon.startsWith('http')) return wrapper(h('img', { src: row.icon, style: 'width:28px;height:28px;border-radius:4px;object-fit:contain;' }));
      return wrapper(h(Icon, { icon: row.icon, color: row.color || undefined, width: '2em', height: '2em' }));
    }
  },
  { title: '排序', key: 'order', width: 70 },
  {
    title: '状态', key: 'status', width: 70,
    render(row) { return h(NTag, { type: row.status ? 'success' : 'error', size: 'small' }, () => row.status ? '启用' : '禁用'); }
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
      <NFormItem label="标题">
        <NInput v-model:value="filters.title" placeholder="标题" clearable @keyup.enter="handleSearch" />
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
      :row-key="(row: Api.Friend.FriendItem) => row.id"
      :scroll-x="800"
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

    <NModal v-model:show="showDialog" preset="dialog" :title="isEdit ? '编辑友链' : '新增友链'" style="width: 600px">
      <NForm label-placement="left" label-width="80px" class="mt-16px">
        <NFormItem label="标题"><NInput v-model:value="formModel.title" placeholder="友链标题" /></NFormItem>
        <NFormItem label="链接">
          <NInputGroup>
            <NInput v-model:value="formModel.href" placeholder="https://" />
            <NButton type="info" :loading="spiderLoading" @click="handleFormSpider">抓取</NButton>
          </NInputGroup>
        </NFormItem>
        <NFormItem label="图标"><IconSelect v-model:value="formModel.icon" :color="formModel.color" /></NFormItem>
        <NFormItem label="颜色"><NColorPicker v-model:value="formModel.color" :modes="['hex']" :show-alpha="false" /></NFormItem>
        <NFormItem label="排序"><NInputNumber v-model:value="formModel.order" :min="0" /></NFormItem>
        <NFormItem label="状态"><NSwitch v-model:value="formModel.status" /></NFormItem>
        <NFormItem label="描述"><NInput v-model:value="formModel.desc" type="textarea" placeholder="描述" /></NFormItem>
      </NForm>
      <template #action>
        <NButton @click="showDialog = false">取消</NButton>
        <NButton type="primary" @click="handleSave">保存</NButton>
      </template>
    </NModal>
  </div>
</template>
