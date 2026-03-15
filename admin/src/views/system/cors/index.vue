<script setup lang="ts">
import { computed, h, nextTick, onBeforeUnmount, reactive, ref } from 'vue';
import {
  NButton, NDataTable, NForm, NFormItem, NInput, NModal, NPagination,
  NPopconfirm, NSelect, NSpace, NSwitch, NTag, type DataTableColumns,
  type FormInst, type FormRules
} from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useDraggable } from 'vue-draggable-plus';
import {
  fetchCorsList, fetchCorsCreate, fetchCorsUpdate,
  fetchCorsDelete, fetchCorsBatchUpdate
} from '@/service/api';

const loading = ref(false);
const tableData = ref<Api.CorsOrigin.CorsItem[]>([]);
const pagination = reactive({ page: 1, pageSize: 20, total: 0 });
const checkedRowKeys = ref<number[]>([]);

const filters = reactive<Api.CorsOrigin.CorsFilter>({
  origin: '', status: null
});
const showDialog = ref(false);
const isEdit = ref(false);
const editId = ref<number | null>(null);

const formModel = reactive({
  origin: '',
  desc: '',
  status: true as boolean
});

const formRef = ref<FormInst | null>(null);
const formRules: FormRules = {
  origin: { required: true, message: '请输入域名', trigger: 'blur' }
};

const statusOptions = [
  { label: '全部', value: null },
  { label: '启用', value: true },
  { label: '禁用', value: false }
];

// Drag sort
const tableRef = ref<InstanceType<typeof NDataTable> | null>(null);

const sortable = useDraggable<Api.CorsOrigin.CorsItem>(ref(undefined), tableData, {
  animation: 150,
  handle: '.drag-handle',
  immediate: false,
  onEnd: handleDragEnd
});

function initSortable() {
  nextTick(() => {
    const el = tableRef.value?.$el as HTMLElement | undefined;
    if (!el) return;
    const tbody = el.querySelector('tbody') as HTMLElement | null;
    if (tbody) {
      try { sortable.destroy(); } catch { /* ignore */ }
      sortable.start(tbody);
    }
  });
}

onBeforeUnmount(() => {
  try { sortable.destroy(); } catch { /* ignore */ }
});

async function handleDragEnd() {
  const updates = tableData.value.map((item, index) => ({
    id: item.id,
    order: index
  }));
  tableData.value.forEach((item, index) => { item.order = index; });
  await fetchCorsBatchUpdate(updates);
  window.$message?.success('排序已保存');
}

async function loadData() {
  loading.value = true;
  const filterData: any = {};
  if (filters.origin) filterData.origin = filters.origin;
  if (filters.status !== null && filters.status !== undefined) filterData.status = filters.status;

  const { data, error } = await fetchCorsList(
    { page: pagination.page, size: pagination.pageSize },
    filterData
  );
  if (!error && data) {
    tableData.value = data.items;
    pagination.total = data.total;
    initSortable();
  }
  loading.value = false;
}

function handleSearch() { pagination.page = 1; loadData(); }
function handleReset() { filters.origin = ''; filters.status = null; handleSearch(); }
function handlePageChange(page: number) { pagination.page = page; loadData(); }
function handlePageSizeChange(size: number) { pagination.pageSize = size; pagination.page = 1; loadData(); }

function handleAdd() {
  isEdit.value = false;
  editId.value = null;
  Object.assign(formModel, { origin: '', desc: '', status: true });
  showDialog.value = true;
}

function handleEdit(row: Api.CorsOrigin.CorsItem) {
  isEdit.value = true;
  editId.value = row.id;
  Object.assign(formModel, {
    origin: row.origin,
    desc: row.desc || '',
    status: row.status
  });
  showDialog.value = true;
}

async function handleSave() {
  try { await formRef.value?.validate(); } catch { return; }
  if (isEdit.value && editId.value) {
    await fetchCorsUpdate(editId.value, {
      origin: formModel.origin,
      desc: formModel.desc,
      status: formModel.status
    });
  } else {
    await fetchCorsCreate({
      origin: formModel.origin,
      desc: formModel.desc,
      status: formModel.status
    });
  }
  showDialog.value = false;
  loadData();
}

async function handleDelete(ids: string) { await fetchCorsDelete(ids); loadData(); }

async function handleBatchDelete() {
  if (!checkedRowKeys.value.length) return;
  await fetchCorsDelete(checkedRowKeys.value.join(','));
  checkedRowKeys.value = [];
  loadData();
}

const columns = computed<DataTableColumns<Api.CorsOrigin.CorsItem>>(() => [
  {
    title: '',
    key: 'drag',
    width: 40,
    render() {
      return h('div', { class: 'drag-handle cursor-move flex-center' }, [
        h(Icon, { icon: 'mdi:drag', width: '1.2em', height: '1.2em', class: 'text-gray-400' })
      ]);
    }
  },
  { type: 'selection' },
  { title: 'ID', key: 'id', width: 60 },
  { title: '域名', key: 'origin', ellipsis: { tooltip: true } },
  { title: '备注', key: 'desc', width: 200, ellipsis: { tooltip: true } },
  {
    title: '状态', key: 'status', width: 80,
    render(row) {
      return h(NTag, { type: row.status ? 'success' : 'error', size: 'small' }, () => row.status ? '启用' : '禁用');
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
      <NFormItem label="域名">
        <NInput v-model:value="filters.origin" placeholder="域名" clearable @keyup.enter="handleSearch" />
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
      ref="tableRef"
      v-model:checked-row-keys="checkedRowKeys"
      :columns="columns"
      :data="tableData"
      :loading="loading"
      :row-key="(row: Api.CorsOrigin.CorsItem) => row.id"
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

    <NModal v-model:show="showDialog" preset="dialog" :title="isEdit ? '编辑跨域配置' : '新增跨域配置'" style="width: 500px">
      <NForm ref="formRef" :model="formModel" :rules="formRules" label-placement="left" label-width="60px" class="mt-16px">
        <NFormItem label="域名" path="origin">
          <NInput v-model:value="formModel.origin" placeholder="例如: https://example.com" />
        </NFormItem>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.desc" placeholder="备注说明" />
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
