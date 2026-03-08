<script setup lang="ts">
import { computed, h, nextTick, onBeforeUnmount, reactive, ref } from 'vue';
import type { TreeSelectRenderPrefix } from 'naive-ui';
import { NButton, NCheckbox, NColorPicker, NDataTable, NForm, NFormItem, NIcon, NInput, NInputGroup, NInputNumber, NModal, NPagination, NPopconfirm, NSelect, NSpace, NSpin, NSwitch, NTag, NTree, NTreeSelect, NUpload, type DataTableColumns, type TreeOption, type UploadFileInfo } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useDraggable } from 'vue-draggable-plus';
import { fetchLinkList, fetchLinkCreate, fetchLinkUpdate, fetchLinkDelete, fetchLinkSiteInfo, fetchLinkSyncCdn, fetchLinkSyncCdnFile, fetchLinkBatchUpdate, fetchLinkSyncCdnBatch, fetchLinkImport, fetchLinkImportJson, fetchMenuTree } from '@/service/api';
import { getServiceBaseURL } from '@/utils/service';
import { getAuthorization } from '@/service/request/shared';

// State
const loading = ref(false);
const tableData = ref<Api.Links.LinkItem[]>([]);
const pagination = reactive({ page: 1, pageSize: 20, total: 0 });
const checkedRowKeys = ref<number[]>([]);

// Filters
const filters = reactive<Api.Links.LinkFilter>({ title: '', href: '', status: null, menus: [] });

// Menu tree for filter and form
const menuTreeData = ref<any[]>([]);

// Dialog
const showDialog = ref(false);
const isEdit = ref(false);
const editId = ref<number | null>(null);
const formModel = reactive<Api.Links.LinkCreate>({
  title: '', href: '', icon: '', is_self: false, is_vip: false,
  desc: '', color: '', order: 0, status: true, menus: []
});

const statusOptions = [
  { label: '全部', value: null },
  { label: '启用', value: true },
  { label: '禁用', value: false }
];

// Drag sort
const tableRef = ref<InstanceType<typeof NDataTable> | null>(null);

const sortable = useDraggable<Api.Links.LinkItem>(ref(undefined), tableData, {
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
  tableData.value.forEach((item, index) => {
    item.order = index;
  });
  await fetchLinkBatchUpdate(updates);
  window.$message?.success('排序已保存');
}

// Load menu tree
async function loadMenuTree() {
  const { data, error } = await fetchMenuTree();
  if (!error && data) {
    menuTreeData.value = buildTreeOptions(data);
  }
}

function buildTreeOptions(items: Api.NavMenu.MenuTreeNode[]): any[] {
  return items.map(item => ({
    key: item.id,
    label: item.title,
    icon: item.icon,
    color: item.color,
    children: item.children?.length ? buildTreeOptions(item.children) : undefined
  }));
}

// Render colored icon prefix for tree-select options
const renderMenuPrefix: TreeSelectRenderPrefix = ({ option }) => {
  const icon = option.icon as string;
  const color = option.color as string;
  if (!icon) return null;
  return h(Icon, { icon, color: color || undefined, style: 'font-size:16px;margin-right:4px;' });
};

// Load data
async function loadData() {
  loading.value = true;
  const filterData: any = {};
  if (filters.title) filterData.title = filters.title;
  if (filters.href) filterData.href = filters.href;
  if (filters.status !== null && filters.status !== undefined) filterData.status = filters.status;
  if (filters.menus?.length) filterData.menus = filters.menus;

  const { data, error } = await fetchLinkList(
    { page: pagination.page, size: pagination.pageSize },
    filterData,
    'order'
  );
  if (!error && data) {
    tableData.value = data.items;
    pagination.total = data.total;
    initSortable();
  }
  loading.value = false;
}

function handleSearch() {
  pagination.page = 1;
  loadData();
}

function handleReset() {
  filters.title = '';
  filters.href = '';
  filters.status = null;
  filters.menus = [];
  handleSearch();
}

function handlePageChange(page: number) {
  pagination.page = page;
  loadData();
}

function handlePageSizeChange(pageSize: number) {
  pagination.pageSize = pageSize;
  pagination.page = 1;
  loadData();
}

// CRUD
function handleAdd() {
  isEdit.value = false;
  editId.value = null;
  Object.assign(formModel, {
    title: '', href: '', icon: '', is_self: false, is_vip: false,
    desc: '', color: '', order: 0, status: true, menus: []
  });
  showDialog.value = true;
}

function handleEdit(row: Api.Links.LinkItem) {
  isEdit.value = true;
  editId.value = row.id;
  Object.assign(formModel, {
    title: row.title,
    href: row.href,
    icon: row.icon || '',
    is_self: row.is_self,
    is_vip: row.is_vip,
    desc: row.desc || '',
    color: row.color || '',
    order: row.order || 0,
    status: row.status,
    menus: row.menus?.map(m => m.id) || []
  });
  showDialog.value = true;
}

async function handleSave() {
  if (isEdit.value && editId.value) {
    await fetchLinkUpdate(editId.value, formModel);
  } else {
    await fetchLinkCreate(formModel);
  }
  showDialog.value = false;
  loadData();
}

async function handleDelete(ids: string) {
  await fetchLinkDelete(ids);
  loadData();
}

async function handleBatchDelete() {
  if (!checkedRowKeys.value.length) return;
  await fetchLinkDelete(checkedRowKeys.value.join(','));
  checkedRowKeys.value = [];
  loadData();
}

// Batch CDN sync
const cdnSyncLoading = ref(false);
function handleBatchCdnSync() {
  if (!checkedRowKeys.value.length || cdnSyncLoading.value) return;
  cdnSyncLoading.value = true;
  fetchLinkSyncCdnBatch(checkedRowKeys.value).then(({ data, error }) => {
    cdnSyncLoading.value = false;
    if (!error && data) {
      const msg = `同步完成：成功 ${data.success} 个，失败 ${data.fail} 个`;
      if (data.fail > 0) {
        const reasons = data.fail_items.map(item => `${item.title}: ${item.reason}`).join('\n');
        window.$message?.warning(`${msg}\n${reasons}`, { duration: 5000 });
      } else {
        window.$message?.success(msg);
      }
      checkedRowKeys.value = [];
      loadData();
    }
  });
}

// Export / Import
const isHttpProxy = import.meta.env.DEV && import.meta.env.VITE_HTTP_PROXY === 'Y';
const { baseURL } = getServiceBaseURL(import.meta.env, isHttpProxy);

// --- Export Dialog ---
const showExportDialog = ref(false);
const exportData = ref<any[]>([]);
const exportLoading = ref(false);
const exportCheckedKeys = ref<string[]>([]);

const exportTreeData = computed<TreeOption[]>(() => {
  const menuMap = new Map<string, any[]>();
  const noMenu: any[] = [];

  for (const link of exportData.value) {
    if (!link.menus?.length) {
      noMenu.push(link);
    } else {
      for (const menuTitle of link.menus) {
        if (!menuMap.has(menuTitle)) menuMap.set(menuTitle, []);
        menuMap.get(menuTitle)!.push(link);
      }
    }
  }

  const tree: TreeOption[] = [];
  for (const [menuTitle, links] of menuMap) {
    tree.push({
      key: `menu:${menuTitle}`,
      label: `${menuTitle} (${links.length})`,
      children: links.map(l => ({
        key: `link:${menuTitle}:${l.title}`,
        label: `${l.title} - ${l.href}`,
        isLeaf: true
      }))
    });
  }
  if (noMenu.length) {
    tree.push({
      key: 'menu:__uncategorized__',
      label: `未分类 (${noMenu.length})`,
      children: noMenu.map(l => ({
        key: `link:__uncategorized__:${l.title}`,
        label: `${l.title} - ${l.href}`,
        isLeaf: true
      }))
    });
  }
  return tree;
});

const exportSelectedCount = computed(() => {
  const titles = new Set(
    exportCheckedKeys.value
      .filter(k => k.startsWith('link:'))
      .map(k => k.slice(k.indexOf(':', 5) + 1))
  );
  return titles.size;
});

function getAllLeafKeys(nodes: TreeOption[]): string[] {
  const keys: string[] = [];
  for (const node of nodes) {
    if (node.children?.length) {
      keys.push(...getAllLeafKeys(node.children));
    } else if (node.key) {
      keys.push(String(node.key));
    }
  }
  return keys;
}

async function handleExport() {
  showExportDialog.value = true;
  exportLoading.value = true;
  const token = getAuthorization();
  const url = `${baseURL}/links/export`;
  try {
    const res = await fetch(url, { headers: { Authorization: token || '' } });
    exportData.value = await res.json();
    // Pre-select all
    exportCheckedKeys.value = getAllLeafKeys(exportTreeData.value);
  } catch {
    window.$message?.error('获取导出数据失败');
  }
  exportLoading.value = false;
}

function handleExportSelectAll() {
  exportCheckedKeys.value = getAllLeafKeys(exportTreeData.value);
}

function handleExportDeselectAll() {
  exportCheckedKeys.value = [];
}

function handleExportConfirm() {
  const selectedTitles = new Set(
    exportCheckedKeys.value
      .filter(k => k.startsWith('link:'))
      .map(k => k.slice(k.indexOf(':', 5) + 1))
  );
  const filtered = exportData.value.filter(item => selectedTitles.has(item.title));
  if (!filtered.length) {
    window.$message?.warning('请至少选择一个链接');
    return;
  }
  const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'links.json';
  a.click();
  URL.revokeObjectURL(a.href);
  showExportDialog.value = false;
}

// --- Import Preview Dialog ---
const importFileRef = ref<HTMLInputElement | null>(null);
const importLoading = ref(false);
const showImportPreview = ref(false);
const importPreviewData = ref<any[]>([]);
const importCheckedKeys = ref<number[]>([]);
const importExistingTitles = ref<Set<string>>(new Set());

interface MenuMapping {
  menuTitle: string;
  action: 'create' | 'map' | 'skip';
  mapToMenuId: number | null;
}
const missingMenuMappings = ref<MenuMapping[]>([]);

const menuMappingActionOptions = [
  { label: '自动创建', value: 'create' },
  { label: '映射到已有菜单', value: 'map' },
  { label: '跳过', value: 'skip' }
];

function handleImportClick() {
  importFileRef.value?.click();
}

function collectMenuTitlesFromTree(nodes: any[]): Set<string> {
  const titles = new Set<string>();
  for (const n of nodes) {
    if (n.label) titles.add(n.label);
    if (n.title) titles.add(n.title);
    if (n.children) {
      for (const t of collectMenuTitlesFromTree(n.children)) titles.add(t);
    }
  }
  return titles;
}

async function handleImportFile(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;

  // Parse JSON client-side
  let items: any[];
  try {
    const text = await file.text();
    items = JSON.parse(text);
  } catch {
    window.$message?.error('JSON格式错误');
    if (importFileRef.value) importFileRef.value.value = '';
    return;
  }
  if (!Array.isArray(items)) {
    window.$message?.error('数据格式错误，应为数组');
    if (importFileRef.value) importFileRef.value.value = '';
    return;
  }

  // Add _idx for row-key
  importPreviewData.value = items.map((item, idx) => ({ ...item, _idx: idx }));

  // Fetch existing link titles for duplicate detection
  const { data } = await fetchLinkList({ page: 1, size: 9999 }, {}, 'order');
  if (data) {
    importExistingTitles.value = new Set(data.items.map(i => i.title));
  }

  // Detect missing menus
  const allMenuTitlesInJson = new Set<string>();
  items.forEach(item => {
    (item.menus || []).forEach((m: string) => allMenuTitlesInJson.add(m));
  });

  const existingMenuTitles = collectMenuTitlesFromTree(menuTreeData.value);
  const missing = [...allMenuTitlesInJson].filter(t => !existingMenuTitles.has(t));
  missingMenuMappings.value = missing.map(title => ({
    menuTitle: title,
    action: 'create',
    mapToMenuId: null
  }));

  // Pre-select non-duplicate items
  importCheckedKeys.value = importPreviewData.value
    .filter(item => item.title && !importExistingTitles.value.has(item.title))
    .map(item => item._idx);

  showImportPreview.value = true;
  if (importFileRef.value) importFileRef.value.value = '';
}

function handleImportSelectAll() {
  importCheckedKeys.value = importPreviewData.value.map(item => item._idx);
}

function handleImportDeselectAll() {
  importCheckedKeys.value = [];
}

function findMenuTitleById(id: number): string | null {
  function search(nodes: any[]): string | null {
    for (const node of nodes) {
      if (node.key === id) return node.label;
      if (node.children) {
        const found = search(node.children);
        if (found) return found;
      }
    }
    return null;
  }
  return search(menuTreeData.value);
}

async function handleImportConfirm() {
  // Validate menu mappings
  const invalidMapping = missingMenuMappings.value.find(
    m => m.action === 'map' && !m.mapToMenuId
  );
  if (invalidMapping) {
    window.$message?.warning(`请为菜单"${invalidMapping.menuTitle}"选择映射目标`);
    return;
  }

  // Build selected items with mapped menus
  const selectedItems = importCheckedKeys.value.map(idx => {
    const raw = importPreviewData.value.find(item => item._idx === idx);
    if (!raw) return null;
    const item = { ...raw };
    delete item._idx;
    if (item.menus) {
      item.menus = item.menus.flatMap((menuTitle: string) => {
        const mapping = missingMenuMappings.value.find(m => m.menuTitle === menuTitle);
        if (!mapping) return [menuTitle];
        if (mapping.action === 'skip') return [];
        if (mapping.action === 'create') return [menuTitle];
        if (mapping.action === 'map' && mapping.mapToMenuId) {
          const mappedTitle = findMenuTitleById(mapping.mapToMenuId);
          return mappedTitle ? [mappedTitle] : [];
        }
        return [menuTitle];
      });
    }
    return item;
  }).filter(Boolean);

  // Collect menus to auto-create
  const menusToCreate = missingMenuMappings.value
    .filter(m => m.action === 'create')
    .map(m => m.menuTitle);

  importLoading.value = true;
  const { data, error } = await fetchLinkImportJson({
    items: selectedItems,
    create_menus: menusToCreate
  });
  importLoading.value = false;

  if (!error && data) {
    window.$message?.success(`导入完成：新增 ${data.created} 个，跳过 ${data.skipped} 个`);
    showImportPreview.value = false;
    loadData();
    loadMenuTree();
  }
}

const importPreviewColumns = computed<DataTableColumns<any>>(() => [
  { type: 'selection' },
  { title: '标题', key: 'title', width: 150, ellipsis: { tooltip: true } },
  { title: '链接', key: 'href', width: 200, ellipsis: { tooltip: true } },
  {
    title: '菜单',
    key: 'menus',
    width: 180,
    render(row: any) {
      const menus = row.menus || [];
      if (!menus.length) return '';
      return h(NSpace, { size: 4 }, () =>
        menus.map((m: string) => {
          const isMissing = missingMenuMappings.value.some(mm => mm.menuTitle === m);
          return h(NTag, { size: 'small', type: isMissing ? 'warning' : 'info' }, () => m);
        })
      );
    }
  },
  {
    title: '状态',
    key: '_import_status',
    width: 100,
    render(row: any) {
      const exists = importExistingTitles.value.has(row.title);
      return h(NTag, { size: 'small', type: exists ? 'default' : 'success' }, () => exists ? '已存在' : '新增');
    }
  }
]);

// Batch edit
const showBatchEdit = ref(false);
const batchEditEnabled = reactive<Record<string, boolean>>({
  color: false, menus: false, is_vip: false, status: false
});
const batchEditModel = reactive({
  color: '', menus: [] as number[], is_vip: false, status: true
});

function handleBatchEditOpen() {
  Object.keys(batchEditEnabled).forEach(k => (batchEditEnabled[k] = false));
  Object.assign(batchEditModel, { color: '', menus: [], is_vip: false, status: true });
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
  await fetchLinkBatchUpdate(updates);
  showBatchEdit.value = false;
  checkedRowKeys.value = [];
  window.$message?.success('批量修改成功');
  loadData();
}

// Spider in form (fetch site info and fill form fields)
const spiderLoading = ref(false);
async function handleFormSpider() {
  if (!formModel.href) {
    window.$message?.warning('请先输入链接地址');
    return;
  }
  spiderLoading.value = true;
  const { data, error } = await fetchLinkSiteInfo(formModel.href);
  if (!error && data) {
    if (data.title) formModel.title = data.title;
    if (data.icon) formModel.icon = data.icon;
    if (data.desc) formModel.desc = data.desc;
    window.$message?.success('抓取成功');
  }
  spiderLoading.value = false;
}

// Columns
const columns = computed<DataTableColumns<Api.Links.LinkItem>>(() => [
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
  { title: '标题', key: 'title', width: 150, ellipsis: { tooltip: true } },
  { title: '链接', key: 'href', width: 200, ellipsis: { tooltip: true } },
  {
    title: '图标',
    key: 'icon',
    width: 60,
    render(row) {
      if (!row.icon) return '';
      const wrapper = (child: any) =>
        h('div', { style: 'display:flex;align-items:center;justify-content:center;width:28px;height:28px;' }, child);
      if (row.icon.startsWith('http')) {
        return wrapper(h('img', { src: row.icon, style: 'width:28px;height:28px;border-radius:4px;object-fit:contain;' }));
      }
      return wrapper(h(Icon, { icon: row.icon, color: row.color || undefined, width: '2em', height: '2em' }));
    }
  },
  {
    title: '菜单',
    key: 'menus',
    width: 150,
    render(row) {
      return h(NSpace, { size: 4 }, () =>
        (row.menus || []).map(m => h(NTag, { size: 'small', type: 'info' }, () => m.title))
      );
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
          { onPositiveClick: () => handleDelete(String(row.id)) },
          {
            trigger: () => h(NButton, { size: 'small', type: 'error' }, () => '删除'),
            default: () => '确定删除？'
          }
        )
      ]);
    }
  }
]);

// Init
loadData();
loadMenuTree();
</script>

<template>
  <div class="flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <!-- Filter Bar -->
    <NForm inline label-placement="left" class="gap-12px">
      <NFormItem label="标题">
        <NInput v-model:value="filters.title" placeholder="标题" clearable @keyup.enter="handleSearch" />
      </NFormItem>
      <NFormItem label="链接">
        <NInput v-model:value="filters.href" placeholder="链接地址" clearable @keyup.enter="handleSearch" />
      </NFormItem>
      <NFormItem label="状态">
        <NSelect v-model:value="filters.status" :options="statusOptions" style="width: 100px" />
      </NFormItem>
      <NFormItem label="菜单">
        <NTreeSelect
          v-model:value="filters.menus"
          :options="menuTreeData"
          multiple
          clearable
          placeholder="选择菜单"
          :max-tag-count="2"
          :render-prefix="renderMenuPrefix"
          style="min-width: 200px"
        />
      </NFormItem>
      <NFormItem>
        <NSpace>
          <NButton type="primary" @click="handleSearch">搜索</NButton>
          <NButton @click="handleReset">重置</NButton>
        </NSpace>
      </NFormItem>
    </NForm>

    <!-- Toolbar -->
    <NSpace class="mb-12px">
      <NButton type="primary" @click="handleAdd">新增</NButton>
      <NPopconfirm @positive-click="handleBatchDelete">
        <template #trigger>
          <NButton type="error" :disabled="!checkedRowKeys.length">批量删除</NButton>
        </template>
        确定删除选中的 {{ checkedRowKeys.length }} 项？
      </NPopconfirm>
      <NPopconfirm @positive-click="handleBatchCdnSync">
        <template #trigger>
          <NButton type="warning" :disabled="!checkedRowKeys.length" :loading="cdnSyncLoading">同步图标到CDN</NButton>
        </template>
        确定将选中的 {{ checkedRowKeys.length }} 个链接的图标同步到CDN？
      </NPopconfirm>
      <NButton @click="handleExport">导出</NButton>
      <NButton :loading="importLoading" @click="handleImportClick">导入</NButton>
      <NButton type="info" :disabled="!checkedRowKeys.length" @click="handleBatchEditOpen">批量编辑</NButton>
      <input ref="importFileRef" type="file" accept=".json" style="display:none" @change="handleImportFile">
    </NSpace>

    <!-- Table -->
    <NDataTable
      ref="tableRef"
      v-model:checked-row-keys="checkedRowKeys"
      :columns="columns"
      :data="tableData"
      :loading="loading"
      :row-key="(row: Api.Links.LinkItem) => row.id"
      :scroll-x="960"
      flex-height
      class="flex-1-hidden"
    />

    <!-- Pagination -->
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

    <!-- Edit Dialog -->
    <NModal v-model:show="showDialog" preset="dialog" :title="isEdit ? '编辑链接' : '新增链接'" style="width: 650px">
      <NForm label-placement="left" label-width="80px" class="mt-16px">
        <NFormItem label="标题">
          <NInput v-model:value="formModel.title" placeholder="链接标题" />
        </NFormItem>
        <NFormItem label="链接">
          <NInputGroup>
            <NInput v-model:value="formModel.href" placeholder="https://" />
            <NButton type="info" :loading="spiderLoading" @click="handleFormSpider">抓取</NButton>
          </NInputGroup>
        </NFormItem>
        <NFormItem label="图标">
          <IconSelect v-model:value="formModel.icon" :color="formModel.color" />
        </NFormItem>
        <NFormItem label="颜色">
          <NColorPicker v-model:value="formModel.color" :modes="['hex']" :show-alpha="false" />
        </NFormItem>
        <NFormItem label="菜单">
          <NTreeSelect
            v-model:value="formModel.menus"
            :options="menuTreeData"
            multiple
            clearable
            placeholder="选择所属菜单"
            :render-prefix="renderMenuPrefix"
          />
        </NFormItem>
        <NFormItem label="排序">
          <NInputNumber v-model:value="formModel.order" :min="0" />
        </NFormItem>
        <NFormItem label="站内打开">
          <NSwitch v-model:value="formModel.is_self" />
        </NFormItem>
        <NFormItem label="VIP">
          <NSwitch v-model:value="formModel.is_vip" />
        </NFormItem>
        <NFormItem label="状态">
          <NSwitch v-model:value="formModel.status" />
        </NFormItem>
        <NFormItem label="描述">
          <NInput v-model:value="formModel.desc" type="textarea" placeholder="链接描述" />
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
        已选中 {{ checkedRowKeys.length }} 个链接，勾选要修改的字段：
      </div>
      <NForm label-placement="left" label-width="80px">
        <NFormItem label="颜色">
          <div class="flex items-center gap-12px w-full">
            <NCheckbox v-model:checked="batchEditEnabled.color" />
            <NColorPicker v-model:value="batchEditModel.color" :modes="['hex']" :show-alpha="false" :disabled="!batchEditEnabled.color" />
          </div>
        </NFormItem>
        <NFormItem label="菜单">
          <div class="flex items-center gap-12px w-full">
            <NCheckbox v-model:checked="batchEditEnabled.menus" />
            <NTreeSelect
              v-model:value="batchEditModel.menus"
              :options="menuTreeData"
              multiple
              clearable
              placeholder="选择所属菜单"
              :render-prefix="renderMenuPrefix"
              :disabled="!batchEditEnabled.menus"
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
    <NModal v-model:show="showExportDialog" preset="dialog" title="选择导出内容" style="width: 700px">
      <div class="mt-16px">
        <div class="flex items-center justify-between mb-12px">
          <NSpace>
            <NButton size="small" @click="handleExportSelectAll">全选</NButton>
            <NButton size="small" @click="handleExportDeselectAll">取消全选</NButton>
          </NSpace>
          <span class="text-13px text-gray-400">已选: {{ exportSelectedCount }} 个链接</span>
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
    <NModal v-model:show="showImportPreview" preset="dialog" title="导入预览" style="width: 850px">
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
          :max-height="300"
          size="small"
        />

        <!-- Menu Mapping Section -->
        <div v-if="missingMenuMappings.length" class="mt-16px">
          <div class="text-14px font-500 mb-8px" style="color: #f0a020;">
            以下菜单在系统中不存在，请选择处理方式：
          </div>
          <div
            v-for="mapping in missingMenuMappings"
            :key="mapping.menuTitle"
            class="flex items-center gap-12px mb-8px p-8px rounded"
            style="background: rgba(240, 160, 32, 0.06);"
          >
            <NTag type="warning" size="small">{{ mapping.menuTitle }}</NTag>
            <span class="text-gray-400 flex-shrink-0">-></span>
            <NSelect
              v-model:value="mapping.action"
              :options="menuMappingActionOptions"
              size="small"
              style="width: 150px"
            />
            <NTreeSelect
              v-if="mapping.action === 'map'"
              v-model:value="mapping.mapToMenuId"
              :options="menuTreeData"
              size="small"
              clearable
              placeholder="选择目标菜单"
              :render-prefix="renderMenuPrefix"
              style="min-width: 180px"
            />
          </div>
        </div>
      </div>
      <template #action>
        <NButton @click="showImportPreview = false">取消</NButton>
        <NButton type="primary" :loading="importLoading" :disabled="!importCheckedKeys.length" @click="handleImportConfirm">确认导入</NButton>
      </template>
    </NModal>
  </div>
</template>
