import { computed, h, ref, type Ref } from 'vue';
import { NTag, type DataTableColumns, type TreeOption } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { fetchMenuImportJson } from '@/service/api';
import { getServiceBaseURL } from '@/utils/service';
import { getAuthorization } from '@/service/request/shared';
import { createTaskWebSocket } from '@/utils/websocket';

export function useMenuImportExport(
  treeData: Ref<Api.NavMenu.MenuTreeNode[]>,
  loadData: () => Promise<void> | void
) {
  const isHttpProxy = import.meta.env.DEV && import.meta.env.VITE_HTTP_PROXY === 'Y';
  const { baseURL } = getServiceBaseURL(import.meta.env, isHttpProxy);

  // --- Export ---
  const showExportDialog = ref(false);
  const exportData = ref<any[]>([]);
  const exportLoading = ref(false);
  const exportCheckedKeys = ref<string[]>([]);

  const exportTreeData = computed<TreeOption[]>(() => {
    const items = exportData.value;
    const parentMap = new Map<string, any[]>();

    for (const item of items) {
      if (item.parent_title) {
        if (!parentMap.has(item.parent_title)) parentMap.set(item.parent_title, []);
        parentMap.get(item.parent_title)!.push(item);
      }
    }

    const tree: TreeOption[] = [];
    for (const item of items) {
      if (!item.parent_title) {
        const children = parentMap.get(item.title) || [];
        tree.push({
          key: item.title,
          label: children.length ? `${item.title} (${children.length} 个子菜单)` : item.title,
          children: children.length ? children.map(c => ({
            key: c.title,
            label: c.title,
            isLeaf: true
          })) : undefined
        });
      }
    }
    return tree;
  });

  const exportSelectedCount = computed(() => exportCheckedKeys.value.length);

  function getAllMenuLeafKeys(nodes: TreeOption[]): string[] {
    const keys: string[] = [];
    for (const node of nodes) {
      keys.push(String(node.key));
      if (node.children?.length) {
        keys.push(...getAllMenuLeafKeys(node.children));
      }
    }
    return keys;
  }

  async function handleExport() {
    showExportDialog.value = true;
    exportLoading.value = true;
    const token = getAuthorization();
    const url = `${baseURL}/menu/export`;
    try {
      const res = await fetch(url, { headers: { Authorization: token || '' } });
      exportData.value = await res.json();
      exportCheckedKeys.value = getAllMenuLeafKeys(exportTreeData.value);
    } catch {
      window.$message?.error('获取导出数据失败');
    }
    exportLoading.value = false;
  }

  function handleExportSelectAll() {
    exportCheckedKeys.value = getAllMenuLeafKeys(exportTreeData.value);
  }

  function handleExportDeselectAll() {
    exportCheckedKeys.value = [];
  }

  function handleExportConfirm() {
    const selectedTitles = new Set(exportCheckedKeys.value);
    const filtered = exportData.value.filter(item => selectedTitles.has(item.title));
    if (!filtered.length) {
      window.$message?.warning('请至少选择一个菜单');
      return;
    }
    const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'menus.json';
    a.click();
    URL.revokeObjectURL(a.href);
    showExportDialog.value = false;
  }

  // --- Import ---
  const importFileRef = ref<HTMLInputElement | null>(null);
  const importLoading = ref(false);
  const showImportPreview = ref(false);
  const importPreviewData = ref<any[]>([]);
  const importCheckedKeys = ref<number[]>([]);
  const importExistingTitles = ref<Set<string>>(new Set());

  function handleImportClick() {
    importFileRef.value?.click();
  }

  function collectExistingMenuTitles(nodes: Api.NavMenu.MenuTreeNode[]): Set<string> {
    const titles = new Set<string>();
    for (const n of nodes) {
      titles.add(n.title);
      if (n.children) {
        for (const t of collectExistingMenuTitles(n.children)) titles.add(t);
      }
    }
    return titles;
  }

  async function handleImportFile(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;

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

    importPreviewData.value = items.map((item, idx) => ({ ...item, _idx: idx }));
    importExistingTitles.value = collectExistingMenuTitles(treeData.value);

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

  async function handleImportConfirm() {
    const selectedItems = importCheckedKeys.value.map(idx => {
      const raw = importPreviewData.value.find(item => item._idx === idx);
      if (!raw) return null;
      const item = { ...raw };
      delete item._idx;
      return item;
    }).filter(Boolean);

    importLoading.value = true;
    const { data, error } = await fetchMenuImportJson({ items: selectedItems });

    if (error || !data?.task_id) {
      importLoading.value = false;
      return;
    }

    createTaskWebSocket(
      data.task_id,
      (result) => {
        importLoading.value = false;
        window.$message?.success(`导入完成：新增 ${result.created} 个，跳过 ${result.skipped} 个`);
        showImportPreview.value = false;
        loadData();
      },
      (errMsg) => {
        importLoading.value = false;
        window.$message?.error(errMsg || '菜单导入失败');
      }
    );
  }

  const importPreviewColumns = computed<DataTableColumns<any>>(() => [
    { type: 'selection' },
    { title: '标题', key: 'title', width: 150 },
    {
      title: '图标',
      key: 'icon',
      width: 60,
      render(row: any) {
        if (!row.icon) return '';
        return h(Icon, { icon: row.icon, color: row.color || undefined, width: '1.5em', height: '1.5em' });
      }
    },
    {
      title: '父级菜单',
      key: 'parent_title',
      width: 120,
      render(row: any) {
        if (!row.parent_title) return '--';
        const existsInSystem = importExistingTitles.value.has(row.parent_title);
        const existsInBatch = importPreviewData.value.some(
          item => item.title === row.parent_title && importCheckedKeys.value.includes(item._idx)
        );
        const isMissing = !existsInSystem && !existsInBatch;
        return h(NTag, { size: 'small', type: isMissing ? 'warning' : 'default' }, () => row.parent_title);
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

  return {
    // Export
    showExportDialog, exportLoading, exportCheckedKeys,
    exportTreeData, exportSelectedCount,
    handleExport, handleExportSelectAll, handleExportDeselectAll, handleExportConfirm,
    // Import
    importFileRef, importLoading, showImportPreview, importPreviewData,
    importCheckedKeys, importPreviewColumns,
    handleImportClick, handleImportFile, handleImportSelectAll, handleImportDeselectAll, handleImportConfirm,
  };
}
