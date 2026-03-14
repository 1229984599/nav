<script setup lang="ts">
import { computed, h, nextTick, onBeforeUnmount, reactive, ref, watch } from 'vue';
import type { SelectRenderLabel } from 'naive-ui';
import { NButton, NCheckbox, NColorPicker, NDataTable, NForm, NFormItem, NInput, NInputNumber, NModal, NPopconfirm, NRadio, NRadioGroup, NSelect, NSpace, NSpin, NSwitch, NTag, NTree, type DataTableColumns, type FormInst, type FormRules } from 'naive-ui';
import { Icon } from '@iconify/vue';
import Sortable from 'sortablejs';
import { fetchMenuTree, fetchMenuCreate, fetchMenuUpdate, fetchMenuDelete, fetchMenuBatchUpdate, fetchMenuImpact } from '@/service/api';
import { useMenuImportExport } from './composables/useMenuImportExport';

const loading = ref(false);
const treeData = ref<Api.NavMenu.MenuTreeNode[]>([]);
const showDialog = ref(false);
const isEdit = ref(false);
const editId = ref<number | null>(null);
const checkedRowKeys = ref<number[]>([]);

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

const formRef = ref<FormInst | null>(null);
const formRules: FormRules = {
  title: { required: true, message: '请输入菜单标题', trigger: 'blur' }
};

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

// Drag sort
const tableRef = ref<InstanceType<typeof NDataTable> | null>(null);

// Flatten tree into the same order as NDataTable's expanded rows
interface FlatItem {
  id: number;
  isParent: boolean;
  parentId: number | null; // actual parent menu id (null for top-level)
}

function buildFlatItems(): FlatItem[] {
  const flat: FlatItem[] = [];
  filteredData.value.forEach(parent => {
    flat.push({ id: parent.id, isParent: true, parentId: null });
    if (parent.children?.length) {
      parent.children.forEach(child => {
        flat.push({ id: child.id, isParent: false, parentId: parent.id });
      });
    }
  });
  return flat;
}

function computeAndSaveOrder(oldIdx: number, newIdx: number) {
  const flat = buildFlatItems();
  const movedItem = flat[oldIdx];
  if (!movedItem) return;

  if (movedItem.isParent) {
    // --- Reorder top-level parents ---
    // Find which parent position the item was dragged from and to
    const parentIndices = flat.map((item, i) => item.isParent ? i : -1).filter(i => i !== -1);
    const parentOldPos = parentIndices.indexOf(oldIdx);
    if (parentOldPos === -1) { loadData(); return; }

    // Map newIdx to the closest parent position:
    // Find which parent "slot" the newIdx falls into
    let parentNewPos: number;
    if (newIdx <= parentIndices[0]) {
      parentNewPos = 0;
    } else {
      // Find the last parent index that is <= newIdx
      parentNewPos = 0;
      for (let i = 0; i < parentIndices.length; i++) {
        if (parentIndices[i] <= newIdx) {
          parentNewPos = i;
        }
      }
    }
    if (parentOldPos === parentNewPos) return;

    // Move within treeData array
    const arr = [...treeData.value];
    const [removed] = arr.splice(parentOldPos, 1);
    arr.splice(parentNewPos, 0, removed);

    // Assign sequential order to all parents
    const updates: Array<{ id: number; order: number }> = arr.map((item, i) => ({ id: item.id, order: i }));
    fetchMenuBatchUpdate(updates).then(() => {
      window.$message?.success('排序已保存');
      loadData();
    });
  } else {
    // --- Reorder children within the same parent ---
    const parentNode = treeData.value.find(p => p.id === movedItem.parentId);
    if (!parentNode?.children?.length) { loadData(); return; }

    // Map flat indices to child-local indices within this parent
    const childFlatIndices: number[] = [];
    flat.forEach((item, i) => {
      if (!item.isParent && item.parentId === movedItem.parentId) {
        childFlatIndices.push(i);
      }
    });
    const childOldPos = childFlatIndices.indexOf(oldIdx);
    if (childOldPos === -1) { loadData(); return; }

    // Map newIdx to the closest child position within same parent
    let childNewPos: number;
    if (newIdx <= childFlatIndices[0]) {
      childNewPos = 0;
    } else if (newIdx >= childFlatIndices[childFlatIndices.length - 1]) {
      childNewPos = childFlatIndices.length - 1;
    } else {
      childNewPos = 0;
      for (let i = 0; i < childFlatIndices.length; i++) {
        if (childFlatIndices[i] <= newIdx) {
          childNewPos = i;
        }
      }
    }

    // If dragged outside this parent's child range, reject
    const parentFlatIdx = flat.findIndex(item => item.isParent && item.id === movedItem.parentId);
    const nextParentFlatIdx = flat.findIndex((item, i) => i > parentFlatIdx && item.isParent);
    const childRangeEnd = nextParentFlatIdx === -1 ? flat.length : nextParentFlatIdx;
    if (newIdx <= parentFlatIdx || newIdx >= childRangeEnd) {
      loadData();
      return;
    }

    if (childOldPos === childNewPos) return;

    // Move within children array
    const children = [...parentNode.children];
    const [removed] = children.splice(childOldPos, 1);
    children.splice(childNewPos, 0, removed);

    // Assign sequential order to all children of this parent
    const updates: Array<{ id: number; order: number }> = children.map((item, i) => ({ id: item.id, order: i }));
    fetchMenuBatchUpdate(updates).then(() => {
      window.$message?.success('排序已保存');
      loadData();
    });
  }
}

let sortableInstance: Sortable | null = null;

function initSortable() {
  nextTick(() => {
    const el = tableRef.value?.$el as HTMLElement | undefined;
    if (!el) return;
    const tbody = el.querySelector('.n-data-table-tbody') as HTMLElement
      || el.querySelector('tbody') as HTMLElement;
    if (!tbody) return;

    if (sortableInstance) {
      try { sortableInstance.destroy(); } catch { /* ignore */ }
      sortableInstance = null;
    }

    sortableInstance = Sortable.create(tbody, {
      animation: 150,
      handle: '.drag-handle',
      onEnd(evt) {
        const oldIdx = evt.oldIndex;
        const newIdx = evt.newIndex;
        if (oldIdx == null || newIdx == null || oldIdx === newIdx) return;
        computeAndSaveOrder(oldIdx, newIdx);
      }
    });
  });
}

onBeforeUnmount(() => {
  if (sortableInstance) {
    try { sortableInstance.destroy(); } catch { /* ignore */ }
    sortableInstance = null;
  }
});

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

const isFilterActive = computed(() => !!filterTitle.value || (filterStatus.value !== null && filterStatus.value !== undefined));

// Re-init sortable whenever the table re-renders due to data/filter changes
watch(filteredData, () => {
  initSortable();
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
    initSortable();
  }
  loading.value = false;
}

// Export / Import (extracted to composable)
const {
  showExportDialog, exportLoading, exportCheckedKeys,
  exportTreeData, exportSelectedCount,
  handleExport, handleExportSelectAll, handleExportDeselectAll, handleExportConfirm,
  importFileRef, importLoading, showImportPreview, importPreviewData,
  importCheckedKeys, importPreviewColumns,
  handleImportClick, handleImportFile, handleImportSelectAll, handleImportDeselectAll, handleImportConfirm,
} = useMenuImportExport(treeData, loadData);

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
  try {
    await formRef.value?.validate();
  } catch {
    return;
  }
  if (isEdit.value && editId.value) {
    await fetchMenuUpdate(editId.value, formModel);
  } else {
    await fetchMenuCreate(formModel);
  }
  showDialog.value = false;
  loadData();
}

// Delete impact dialog
const showDeleteDialog = ref(false);
const deleteTargetIds = ref<number[]>([]);
const deleteImpact = ref<{ child_count: number; link_count: number; menu_titles: string[] }>({ child_count: 0, link_count: 0, menu_titles: [] });
const deleteChildrenAction = ref<'move_up' | 'delete'>('move_up');
const deleteLinksAction = ref<'unlink' | 'delete'>('unlink');
const deleteLoading = ref(false);

async function handleDelete(id: number) {
  await showDeleteImpactDialog([id]);
}

async function handleBatchDelete() {
  if (!checkedRowKeys.value.length) return;
  await showDeleteImpactDialog([...checkedRowKeys.value]);
}

async function showDeleteImpactDialog(ids: number[]) {
  deleteTargetIds.value = ids;
  deleteChildrenAction.value = 'move_up';
  deleteLinksAction.value = 'unlink';

  const { data, error } = await fetchMenuImpact(ids.join(','));
  if (error || !data) {
    window.$message?.error('查询影响失败');
    return;
  }
  deleteImpact.value = data;

  // If no children and no links, delete directly
  if (data.child_count === 0 && data.link_count === 0) {
    await executeDelete();
    return;
  }

  showDeleteDialog.value = true;
}

async function executeDelete() {
  deleteLoading.value = true;
  await fetchMenuDelete(
    deleteTargetIds.value.join(','),
    deleteChildrenAction.value,
    deleteLinksAction.value
  );
  deleteLoading.value = false;
  showDeleteDialog.value = false;
  checkedRowKeys.value = [];
  loadData();
}

// Batch edit
const showBatchEdit = ref(false);
const batchEditEnabled = reactive<Record<string, boolean>>({
  color: false, parent_id: false, is_vip: false, status: false
});
const batchEditModel = reactive({
  color: '', parent_id: null as number | null, is_vip: false, status: true
});

function handleBatchEditOpen() {
  Object.keys(batchEditEnabled).forEach(k => (batchEditEnabled[k] = false));
  Object.assign(batchEditModel, { color: '', parent_id: null, is_vip: false, status: true });
  showBatchEdit.value = true;
}

async function handleBatchEditSave() {
  const enabledFields = Object.keys(batchEditEnabled).filter(k => batchEditEnabled[k]);
  if (!enabledFields.length) {
    window.$message?.warning('请至少勾选一个要修改的字段');
    return;
  }
  const updates = checkedRowKeys.value.map(id => {
    const item: Record<string, any> = { id };
    enabledFields.forEach(field => {
      item[field] = (batchEditModel as any)[field];
    });
    return item;
  });
  await fetchMenuBatchUpdate(updates);
  showBatchEdit.value = false;
  checkedRowKeys.value = [];
  window.$message?.success('批量修改成功');
  loadData();
}

const columns = computed<DataTableColumns<Api.NavMenu.MenuTreeNode>>(() => [
  {
    title: '',
    key: 'drag',
    width: 40,
    render() {
      if (isFilterActive.value) {
        return h('div');
      }
      return h('div', { class: 'drag-handle cursor-move flex-center' }, [
        h(Icon, { icon: 'mdi:drag', width: '1.2em', height: '1.2em', class: 'text-gray-400' })
      ]);
    }
  },
  { type: 'selection' },
  {
    title: 'ID',
    key: 'id',
    width: 80,
    render(row) {
      if (row.parent_id) {
        const parent = treeData.value.find(p => p.id === row.parent_id);
        return h('div', { style: 'display:flex;align-items:center;gap:4px;' }, [
          h('span', null, String(row.id)),
          h(NTag, { size: 'tiny', type: 'info', bordered: false }, () => parent ? parent.title : '子')
        ]);
      }
      return h('span', { style: 'font-weight:600;' }, String(row.id));
    }
  },
  {
    title: '标题',
    key: 'title',
    width: 200,
    render(row) {
      if (row.parent_id) {
        return h('div', { style: 'display:flex;align-items:center;gap:6px;padding-left:20px;' }, [
          h('span', { style: 'color:#18a058;font-size:14px;line-height:1;' }, '├─'),
          h('span', null, row.title)
        ]);
      }
      return h('div', { style: 'display:flex;align-items:center;gap:6px;' }, [
        h(Icon, { icon: 'mdi:folder-outline', width: '16px', height: '16px', style: 'color:#f0a020;flex-shrink:0;' }),
        h('span', { style: 'font-weight:600;' }, row.title)
      ]);
    }
  },
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
        h(NButton, { size: 'small', type: 'error', onClick: () => handleDelete(row.id) }, () => '删除')
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
        <NSpace>
          <NButton type="primary" @click="handleAdd">新增</NButton>
          <NButton type="error" :disabled="!checkedRowKeys.length" @click="handleBatchDelete">批量删除</NButton>
          <NButton type="info" :disabled="!checkedRowKeys.length" @click="handleBatchEditOpen">批量编辑</NButton>
          <NButton @click="handleExport">导出</NButton>
          <NButton :loading="importLoading" @click="handleImportClick">导入</NButton>
          <input ref="importFileRef" type="file" accept=".json" style="display:none" @change="handleImportFile">
        </NSpace>
      </NFormItem>
    </NForm>

    <NDataTable
      ref="tableRef"
      v-model:checked-row-keys="checkedRowKeys"
      :columns="columns"
      :data="filteredData"
      :loading="loading"
      :row-key="(row: Api.NavMenu.MenuTreeNode) => row.id"
      :row-class-name="(row: Api.NavMenu.MenuTreeNode) => row.parent_id ? 'child-row' : 'parent-row'"
      default-expand-all
      :scroll-x="600"
      flex-height
      class="flex-1-hidden"
    />

    <NModal v-model:show="showDialog" preset="dialog" :title="isEdit ? '编辑菜单' : '新增菜单'" style="width: 600px">
      <NForm ref="formRef" :model="formModel" :rules="formRules" label-placement="left" label-width="80px" class="mt-16px">
        <NFormItem label="标题" path="title">
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

    <!-- Batch Edit Dialog -->
    <NModal v-model:show="showBatchEdit" preset="dialog" title="批量编辑" style="width: 550px">
      <div class="mt-16px text-13px text-gray-400 mb-12px">
        已选中 {{ checkedRowKeys.length }} 个菜单，勾选要修改的字段：
      </div>
      <NForm label-placement="left" label-width="80px">
        <NFormItem label="颜色">
          <div class="flex items-center gap-12px w-full">
            <NCheckbox v-model:checked="batchEditEnabled.color" />
            <NColorPicker v-model:value="batchEditModel.color" :modes="['hex']" :show-alpha="false" :disabled="!batchEditEnabled.color" />
          </div>
        </NFormItem>
        <NFormItem label="父级菜单">
          <div class="flex items-center gap-12px w-full">
            <NCheckbox v-model:checked="batchEditEnabled.parent_id" />
            <NSelect
              v-model:value="batchEditModel.parent_id"
              :options="parentOptions"
              :render-label="renderParentLabel"
              clearable
              placeholder="选择父级菜单"
              :disabled="!batchEditEnabled.parent_id"
              class="flex-1"
            />
          </div>
        </NFormItem>
        <NFormItem label="VIP">
          <div class="flex items-center gap-12px">
            <NCheckbox v-model:checked="batchEditEnabled.is_vip" />
            <NSwitch v-model:value="batchEditModel.is_vip" :disabled="!batchEditEnabled.is_vip" />
          </div>
        </NFormItem>
        <NFormItem label="状态">
          <div class="flex items-center gap-12px">
            <NCheckbox v-model:checked="batchEditEnabled.status" />
            <NSwitch v-model:value="batchEditModel.status" :disabled="!batchEditEnabled.status" />
          </div>
        </NFormItem>
      </NForm>
      <template #action>
        <NButton @click="showBatchEdit = false">取消</NButton>
        <NButton type="primary" @click="handleBatchEditSave">保存</NButton>
      </template>
    </NModal>

    <!-- Export Dialog -->
    <NModal v-model:show="showExportDialog" preset="dialog" title="选择导出菜单" style="width: 600px">
      <div class="mt-16px">
        <div class="flex items-center justify-between mb-12px">
          <NSpace>
            <NButton size="small" @click="handleExportSelectAll">全选</NButton>
            <NButton size="small" @click="handleExportDeselectAll">取消全选</NButton>
          </NSpace>
          <span class="text-13px text-gray-400">已选: {{ exportSelectedCount }} 个菜单</span>
        </div>
        <NSpin :show="exportLoading">
          <div style="max-height: 400px; overflow-y: auto; border: 1px solid var(--n-border-color, #e0e0e6); border-radius: 4px; padding: 8px;">
            <NTree
              :data="exportTreeData"
              checkable
              cascade
              :checked-keys="exportCheckedKeys"
              block-line
              expand-on-click
              :default-expand-all="true"
              @update:checked-keys="(keys: string[]) => exportCheckedKeys = keys"
            />
          </div>
        </NSpin>
      </div>
      <template #action>
        <NButton @click="showExportDialog = false">取消</NButton>
        <NButton type="primary" :disabled="!exportSelectedCount" @click="handleExportConfirm">导出</NButton>
      </template>
    </NModal>

    <!-- Import Preview Dialog -->
    <NModal v-model:show="showImportPreview" preset="dialog" title="导入预览" style="width: 750px">
      <div class="mt-16px">
        <div class="flex items-center justify-between mb-12px">
          <NSpace>
            <NButton size="small" @click="handleImportSelectAll">全选</NButton>
            <NButton size="small" @click="handleImportDeselectAll">取消全选</NButton>
          </NSpace>
          <span class="text-13px text-gray-400">已选: {{ importCheckedKeys.length }} / {{ importPreviewData.length }} 个</span>
        </div>
        <NDataTable
          v-model:checked-row-keys="importCheckedKeys"
          :columns="importPreviewColumns"
          :data="importPreviewData"
          :row-key="(row: any) => row._idx"
          :max-height="350"
          size="small"
        />
      </div>
      <template #action>
        <NButton @click="showImportPreview = false">取消</NButton>
        <NButton type="primary" :loading="importLoading" :disabled="!importCheckedKeys.length" @click="handleImportConfirm">确认导入</NButton>
      </template>
    </NModal>

    <!-- Delete Impact Dialog -->
    <NModal v-model:show="showDeleteDialog" preset="dialog" title="确认删除" style="width: 500px">
      <div class="mt-16px">
        <div class="mb-12px p-12px rounded" style="background: rgba(240, 160, 32, 0.08); border: 1px solid rgba(240, 160, 32, 0.3); border-radius: 6px;">
          <div class="text-14px" style="color: #f0a020;">
            即将删除菜单：{{ deleteImpact.menu_titles.join('、') }}
          </div>
        </div>

        <div v-if="deleteImpact.child_count > 0" class="mb-16px">
          <div class="text-14px font-500 mb-8px">
            包含 {{ deleteImpact.child_count }} 个子菜单，如何处理？
          </div>
          <NRadioGroup v-model:value="deleteChildrenAction">
            <NSpace vertical>
              <NRadio value="move_up">将子菜单移到上级</NRadio>
              <NRadio value="delete">同时删除子菜单</NRadio>
            </NSpace>
          </NRadioGroup>
        </div>

        <div v-if="deleteImpact.link_count > 0" class="mb-16px">
          <div class="text-14px font-500 mb-8px">
            关联了 {{ deleteImpact.link_count }} 个链接，如何处理？
          </div>
          <NRadioGroup v-model:value="deleteLinksAction">
            <NSpace vertical>
              <NRadio value="unlink">仅取消关联（保留链接）</NRadio>
              <NRadio value="delete">同时删除关联链接</NRadio>
            </NSpace>
          </NRadioGroup>
        </div>
      </div>
      <template #action>
        <NButton @click="showDeleteDialog = false">取消</NButton>
        <NButton type="error" :loading="deleteLoading" @click="executeDelete">确认删除</NButton>
      </template>
    </NModal>
  </div>
</template>

<style scoped>
:deep(.child-row td) {
  background-color: rgba(24, 160, 88, 0.04) !important;
}

:deep(.parent-row td) {
  font-weight: 500;
}
</style>
