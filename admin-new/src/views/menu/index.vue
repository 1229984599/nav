<script setup lang="ts">
import { computed, h, reactive, ref } from 'vue';
import type { SelectRenderLabel } from 'naive-ui';
import { NButton, NColorPicker, NDataTable, NForm, NFormItem, NInput, NInputNumber, NModal, NPopconfirm, NSelect, NSpace, NSwitch, NTag, type DataTableColumns } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { fetchMenuTree, fetchMenuCreate, fetchMenuUpdate, fetchMenuDelete } from '@/service/api';

const loading = ref(false);
const treeData = ref<Api.NavMenu.MenuTreeNode[]>([]);
const showDialog = ref(false);
const isEdit = ref(false);
const editId = ref<number | null>(null);

// Filters
const filterTitle = ref('');
const filterStatus = ref<boolean | null>(null);

const statusOptions = [
  { label: '全部', value: null },
  { label: '启用', value: true },
  { label: '禁用', value: false }
];

// Form
const formModel = reactive<Api.NavMenu.MenuCreate>({
  title: '', icon: 'ic:round-menu', color: '', order: 0,
  is_vip: false, status: true, parent_id: null
});

// Parent menu options for form
const parentOptions = computed(() => {
  return [
    { label: '无（顶级菜单）', value: null },
    ...treeData.value
      .filter(item => !item.parent_id)
      .map(item => ({ label: item.title, value: item.id, icon: item.icon, color: item.color }))
  ];
});

// Render colored icon in parent menu select
const renderParentLabel: SelectRenderLabel = (option) => {
  const icon = option.icon as string | undefined;
  const color = option.color as string | undefined;
  if (!icon) return option.label as string;
  return h('div', { style: 'display:flex;align-items:center;gap:6px;' }, [
    h(Icon, { icon, color: color || undefined, style: 'font-size:16px' }),
    h('span', null, option.label as string)
  ]);
};

// Filtered tree data
const filteredData = computed(() => {
  let data = treeData.value;
  if (filterTitle.value) {
    data = filterTree(data, filterTitle.value);
  }
  if (filterStatus.value !== null && filterStatus.value !== undefined) {
    data = data.filter(node => filterNode(node, filterStatus.value!));
  }
  return data;
});

function filterTree(items: Api.NavMenu.MenuTreeNode[], keyword: string): Api.NavMenu.MenuTreeNode[] {
  return items.reduce<Api.NavMenu.MenuTreeNode[]>((acc, item) => {
    const children = item.children ? filterTree(item.children, keyword) : [];
    if (item.title.includes(keyword) || children.length > 0) {
      acc.push({ ...item, children: children.length ? children : item.children });
    }
    return acc;
  }, []);
}

function filterNode(node: Api.NavMenu.MenuTreeNode, status: boolean): boolean {
  if (node.status === status) return true;
  return (node.children || []).some(child => filterNode(child, status));
}

async function loadData() {
  loading.value = true;
  const { data, error } = await fetchMenuTree();
  if (!error && data) {
    treeData.value = data;
  }
  loading.value = false;
}

function handleAdd() {
  isEdit.value = false;
  editId.value = null;
  Object.assign(formModel, {
    title: '', icon: 'ic:round-menu', color: '', order: 0,
    is_vip: false, status: true, parent_id: null
  });
  showDialog.value = true;
}

function handleEdit(row: Api.NavMenu.MenuTreeNode) {
  isEdit.value = true;
  editId.value = row.id;
  Object.assign(formModel, {
    title: row.title,
    icon: row.icon || '',
    color: row.color || '',
    order: row.order || 0,
    is_vip: row.is_vip,
    status: row.status,
    parent_id: row.parent_id || null
  });
  showDialog.value = true;
}

async function handleSave() {
  if (isEdit.value && editId.value) {
    await fetchMenuUpdate(editId.value, formModel);
  } else {
    await fetchMenuCreate(formModel);
  }
  showDialog.value = false;
  loadData();
}

async function handleDelete(id: number) {
  await fetchMenuDelete(String(id));
  loadData();
}

const columns = computed<DataTableColumns<Api.NavMenu.MenuTreeNode>>(() => [
  { title: 'ID', key: 'id', width: 60 },
  { title: '标题', key: 'title', width: 150 },
  {
    title: '图标',
    key: 'icon',
    width: 60,
    render(row) {
      return h(Icon, { icon: row.icon || 'ic:round-menu', color: row.color || undefined, width: '2em', height: '2em' });
    }
  },
  { title: '排序', key: 'order', width: 70 },
  {
    title: 'VIP',
    key: 'is_vip',
    width: 60,
    render(row) {
      return h(NTag, { type: row.is_vip ? 'warning' : 'default', size: 'small' }, () => row.is_vip ? '是' : '否');
    }
  },
  {
    title: '状态',
    key: 'status',
    width: 70,
    render(row) {
      return h(NTag, { type: row.status ? 'success' : 'error', size: 'small' }, () => row.status ? '启用' : '禁用');
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    render(row) {
      return h(NSpace, { size: 8 }, () => [
        h(NButton, { size: 'small', type: 'primary', onClick: () => handleEdit(row) }, () => '编辑'),
        h(
          NPopconfirm,
          { onPositiveClick: () => handleDelete(row.id) },
          {
            trigger: () => h(NButton, { size: 'small', type: 'error' }, () => '删除'),
            default: () => '确定删除？'
          }
        )
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
        <NInput v-model:value="filterTitle" placeholder="菜单标题" clearable />
      </NFormItem>
      <NFormItem label="状态">
        <NSelect v-model:value="filterStatus" :options="statusOptions" style="width: 100px" />
      </NFormItem>
      <NFormItem>
        <NButton type="primary" @click="handleAdd">新增</NButton>
      </NFormItem>
    </NForm>

    <NDataTable
      :columns="columns"
      :data="filteredData"
      :loading="loading"
      :row-key="(row: Api.NavMenu.MenuTreeNode) => row.id"
      default-expand-all
      :scroll-x="600"
      flex-height
      class="flex-1-hidden"
    />

    <NModal v-model:show="showDialog" preset="dialog" :title="isEdit ? '编辑菜单' : '新增菜单'" style="width: 600px">
      <NForm label-placement="left" label-width="80px" class="mt-16px">
        <NFormItem label="标题">
          <NInput v-model:value="formModel.title" placeholder="菜单标题" />
        </NFormItem>
        <NFormItem label="图标">
          <IconSelect v-model:value="formModel.icon" :color="formModel.color" :show-upload="false" />
        </NFormItem>
        <NFormItem label="颜色">
          <NColorPicker v-model:value="formModel.color" :modes="['hex']" :show-alpha="false" />
        </NFormItem>
        <NFormItem label="父级菜单">
          <NSelect v-model:value="formModel.parent_id" :options="parentOptions" :render-label="renderParentLabel" clearable placeholder="选择父级菜单" />
        </NFormItem>
        <NFormItem label="排序">
          <NInputNumber v-model:value="formModel.order" :min="0" />
        </NFormItem>
        <NFormItem label="VIP">
          <NSwitch v-model:value="formModel.is_vip" />
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
