import { computed, h, ref, type Ref } from 'vue';
import { NSpace, NTag, type DataTableColumns, type TreeOption } from 'naive-ui';
import { fetchLinkImportJson, fetchLinkTitles } from '@/service/api';
import { getServiceBaseURL } from '@/utils/service';
import { getAuthorization } from '@/service/request/shared';
import { createTaskWebSocket } from '@/utils/websocket';

interface MenuImportInfo {
  title: string;
  icon: string;
  color: string | null;
  parent_title: string | null;
}

interface MenuMapping {
  menuTitle: string;
  action: 'create' | 'map' | 'skip';
  mapToMenuId: number | null;
}

interface PendingTask {
  taskId: string;
  type: 'import' | 'cdn_sync';
  startedAt: number;
}

const TASK_STORAGE_KEY = 'nav_pending_tasks';

function menuEntryTitle(m: string | { title: string }): string {
  return typeof m === 'string' ? m : m.title;
}

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

function savePendingTask(task: PendingTask) {
  const tasks = getPendingTasks();
  tasks.push(task);
  localStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(tasks));
}

function getPendingTasks(): PendingTask[] {
  try {
    return JSON.parse(localStorage.getItem(TASK_STORAGE_KEY) || '[]');
  } catch {
    return [];
  }
}

function removePendingTask(taskId: string) {
  const tasks = getPendingTasks().filter(t => t.taskId !== taskId);
  localStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(tasks));
}

export function useLinksImportExport(
  menuTreeData: Ref<any[]>,
  loadData: () => Promise<void> | void,
  loadMenuTree: () => Promise<void> | void,
  cdnSyncLoading: Ref<boolean>
) {
  const isHttpProxy = import.meta.env.DEV && import.meta.env.VITE_HTTP_PROXY === 'Y';
  const { baseURL } = getServiceBaseURL(import.meta.env, isHttpProxy);

  // --- Export ---
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
        for (const me of link.menus) {
          const mt = menuEntryTitle(me);
          if (!menuMap.has(mt)) menuMap.set(mt, []);
          menuMap.get(mt)!.push(link);
        }
      }
    }
    const tree: TreeOption[] = [];
    for (const [mt, links] of menuMap) {
      tree.push({
        key: `menu:${mt}`,
        label: `${mt} (${links.length})`,
        children: links.map(l => ({ key: `link:${mt}:${l.title}`, label: `${l.title} - ${l.href}`, isLeaf: true }))
      });
    }
    if (noMenu.length) {
      tree.push({
        key: 'menu:__uncategorized__',
        label: `未分类 (${noMenu.length})`,
        children: noMenu.map(l => ({ key: `link:__uncategorized__:${l.title}`, label: `${l.title} - ${l.href}`, isLeaf: true }))
      });
    }
    return tree;
  });

  const exportSelectedCount = computed(() => {
    const titles = new Set(exportCheckedKeys.value.filter(k => k.startsWith('link:')).map(k => k.slice(k.indexOf(':', 5) + 1)));
    return titles.size;
  });

  async function handleExport() {
    showExportDialog.value = true;
    exportLoading.value = true;
    const token = getAuthorization();
    const url = `${baseURL}/links/export`;
    try {
      const res = await fetch(url, { headers: { Authorization: token || '' } });
      exportData.value = await res.json();
      exportCheckedKeys.value = getAllLeafKeys(exportTreeData.value);
    } catch {
      window.$message?.error('获取导出数据失败');
    }
    exportLoading.value = false;
  }

  function handleExportSelectAll() { exportCheckedKeys.value = getAllLeafKeys(exportTreeData.value); }
  function handleExportDeselectAll() { exportCheckedKeys.value = []; }

  function handleExportConfirm() {
    const selectedTitles = new Set(exportCheckedKeys.value.filter(k => k.startsWith('link:')).map(k => k.slice(k.indexOf(':', 5) + 1)));
    const filtered = exportData.value.filter(item => selectedTitles.has(item.title));
    if (!filtered.length) { window.$message?.warning('请至少选择一个链接'); return; }
    const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'links.json';
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
  const importProgress = ref<{ current: number; total: number; created: number; skipped: number } | null>(null);
  const importMenuInfoMap = ref<Map<string, MenuImportInfo>>(new Map());
  const missingMenuMappings = ref<MenuMapping[]>([]);

  const menuMappingActionOptions = [
    { label: '自动创建', value: 'create' },
    { label: '映射到已有菜单', value: 'map' },
    { label: '跳过', value: 'skip' }
  ];

  function handleImportClick() { importFileRef.value?.click(); }

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
    const { data } = await fetchLinkTitles();
    if (data) importExistingTitles.value = new Set(data);

    const allMenuTitlesInJson = new Set<string>();
    importMenuInfoMap.value = new Map();
    items.forEach(item => {
      (item.menus || []).forEach((m: string | MenuImportInfo) => {
        const title = menuEntryTitle(m);
        allMenuTitlesInJson.add(title);
        if (typeof m === 'object' && m.title && !importMenuInfoMap.value.has(title)) {
          importMenuInfoMap.value.set(title, { title: m.title, icon: m.icon || 'ic:round-menu', color: m.color || null, parent_title: m.parent_title || null });
        }
      });
    });
    const existingMenuTitles = collectMenuTitlesFromTree(menuTreeData.value);
    const missing = [...allMenuTitlesInJson].filter(t => !existingMenuTitles.has(t));
    missingMenuMappings.value = missing.map(title => ({ menuTitle: title, action: 'create' as const, mapToMenuId: null }));
    importCheckedKeys.value = importPreviewData.value.filter(item => item.title && !importExistingTitles.value.has(item.title)).map(item => item._idx);
    showImportPreview.value = true;
    if (importFileRef.value) importFileRef.value.value = '';
  }

  function handleImportSelectAll() { importCheckedKeys.value = importPreviewData.value.map(item => item._idx); }
  function handleImportDeselectAll() { importCheckedKeys.value = []; }

  function findMenuTitleById(id: number): string | null {
    function search(nodes: any[]): string | null {
      for (const node of nodes) {
        if (node.key === id) return node.label;
        if (node.children) { const found = search(node.children); if (found) return found; }
      }
      return null;
    }
    return search(menuTreeData.value);
  }

  async function handleImportConfirm() {
    const invalidMapping = missingMenuMappings.value.find(m => m.action === 'map' && !m.mapToMenuId);
    if (invalidMapping) { window.$message?.warning(`请为菜单"${invalidMapping.menuTitle}"选择映射目标`); return; }

    const selectedItems = importCheckedKeys.value.map(idx => {
      const raw = importPreviewData.value.find(item => item._idx === idx);
      if (!raw) return null;
      const item = { ...raw };
      delete item._idx;
      if (item.menus) {
        item.menus = item.menus.flatMap((menuEntry: string | any) => {
          const mt = menuEntryTitle(menuEntry);
          const mapping = missingMenuMappings.value.find(m => m.menuTitle === mt);
          if (!mapping) return [mt];
          if (mapping.action === 'skip') return [];
          if (mapping.action === 'create') return [mt];
          if (mapping.action === 'map' && mapping.mapToMenuId) { const mapped = findMenuTitleById(mapping.mapToMenuId); return mapped ? [mapped] : []; }
          return [mt];
        });
      }
      return item;
    }).filter(Boolean);

    const menusToCreate: Array<string | MenuImportInfo> = missingMenuMappings.value
      .filter(m => m.action === 'create')
      .map(m => importMenuInfoMap.value.get(m.menuTitle) || m.menuTitle);

    importLoading.value = true;
    importProgress.value = null;
    const { data, error } = await fetchLinkImportJson({ items: selectedItems, create_menus: menusToCreate });
    if (error || !data?.task_id) { importLoading.value = false; window.$message?.error('启动导入任务失败'); return; }

    window.$message?.info('导入任务已启动...');
    savePendingTask({ taskId: data.task_id, type: 'import', startedAt: Date.now() });
    createTaskWebSocket(
      data.task_id,
      (result) => { importLoading.value = false; importProgress.value = null; removePendingTask(data.task_id); window.$message?.success(`导入完成：新增 ${result.created} 个，跳过 ${result.skipped} 个`); showImportPreview.value = false; loadData(); loadMenuTree(); },
      (errMsg) => { importLoading.value = false; importProgress.value = null; removePendingTask(data.task_id); window.$message?.error(errMsg || '导入失败'); },
      (progress) => { importProgress.value = progress; }
    );
  }

  const importProgressPercent = computed(() => {
    if (!importProgress.value) return 0;
    return Math.round((importProgress.value.current / importProgress.value.total) * 100);
  });

  const importPreviewColumns = computed<DataTableColumns<any>>(() => [
    { type: 'selection' },
    { title: '标题', key: 'title', width: 150, ellipsis: { tooltip: true } },
    { title: '链接', key: 'href', width: 200, ellipsis: { tooltip: true } },
    {
      title: '菜单', key: 'menus', width: 180,
      render(row: any) {
        const menus = row.menus || [];
        if (!menus.length) return '';
        return h(NSpace, { size: 4 }, () =>
          menus.map((m: string | any) => {
            const title = menuEntryTitle(m);
            const isMissing = missingMenuMappings.value.some(mm => mm.menuTitle === title);
            return h(NTag, { size: 'small', type: isMissing ? 'warning' : 'info' }, () => title);
          })
        );
      }
    },
    {
      title: '状态', key: '_import_status', width: 100,
      render(row: any) {
        const exists = importExistingTitles.value.has(row.title);
        return h(NTag, { size: 'small', type: exists ? 'default' : 'success' }, () => exists ? '已存在' : '新增');
      }
    }
  ]);

  function reconnectPendingTasks() {
    const tasks = getPendingTasks();
    const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;
    for (const task of tasks) {
      if (task.startedAt < fiveMinutesAgo) { removePendingTask(task.taskId); continue; }
      if (task.type === 'import') {
        importLoading.value = true; importProgress.value = null;
        window.$message?.info('检测到未完成的导入任务，正在重新连接...');
        createTaskWebSocket(task.taskId,
          (result) => { importLoading.value = false; importProgress.value = null; removePendingTask(task.taskId); window.$message?.success(`导入完成：新增 ${result.created} 个，跳过 ${result.skipped} 个`); showImportPreview.value = false; loadData(); loadMenuTree(); },
          (errMsg) => { importLoading.value = false; importProgress.value = null; removePendingTask(task.taskId); if (errMsg !== 'WebSocket连接失败') window.$message?.error(errMsg || '导入失败'); },
          (progress) => { importProgress.value = progress; }
        );
      } else if (task.type === 'cdn_sync') {
        cdnSyncLoading.value = true;
        window.$message?.info('检测到未完成的CDN同步任务，正在重新连接...');
        createTaskWebSocket(task.taskId,
          (result) => { cdnSyncLoading.value = false; removePendingTask(task.taskId); const msg = `同步完成：成功 ${result.success} 个，失败 ${result.fail} 个`; if (result.fail > 0) { const reasons = result.fail_items.map((item: any) => `${item.title}: ${item.reason}`).join('\n'); window.$message?.warning(`${msg}\n${reasons}`, { duration: 5000 }); } else { window.$message?.success(msg); } loadData(); },
          (errMsg) => { cdnSyncLoading.value = false; removePendingTask(task.taskId); if (errMsg !== 'WebSocket连接失败') window.$message?.error(errMsg || 'CDN同步失败'); }
        );
      }
    }
  }

  return {
    // Export
    showExportDialog, exportData, exportLoading, exportCheckedKeys,
    exportTreeData, exportSelectedCount,
    handleExport, handleExportSelectAll, handleExportDeselectAll, handleExportConfirm,
    // Import
    importFileRef, importLoading, showImportPreview, importPreviewData,
    importCheckedKeys, importProgress, importProgressPercent, importPreviewColumns,
    missingMenuMappings, menuMappingActionOptions,
    handleImportClick, handleImportFile, handleImportSelectAll, handleImportDeselectAll, handleImportConfirm,
    // Task persistence
    savePendingTask, removePendingTask, reconnectPendingTasks,
    // Utils
    menuEntryTitle,
  };
}
