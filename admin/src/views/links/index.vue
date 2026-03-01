<template>
  <el-card>
    <template #header>
      <div class="toolbar">
        <el-input v-model="filters.title" placeholder="标题" clearable @keyup.enter="onSearch" />
        <el-input v-model="filters.href" placeholder="链接" clearable @keyup.enter="onSearch" />
        <el-select v-model="filters.status" placeholder="状态" clearable>
          <el-option :value="true" label="启用" />
          <el-option :value="false" label="禁用" />
        </el-select>
        <el-select v-model="filters.menuId" placeholder="菜单" clearable>
          <el-option v-for="item in menuFlat" :key="item.id" :value="item.id" :label="item.title" />
        </el-select>
        <el-button type="primary" @click="onSearch">查询</el-button>
        <el-button @click="onReset">重置</el-button>
        <el-button type="success" @click="openCreate">新增</el-button>
        <el-button type="danger" :disabled="!selectedIds.length" @click="onBatchDelete">批量删除</el-button>
      </div>
    </template>

    <el-table ref="tableRef" :data="tableData" v-loading="loading" style="width: 100%" @selection-change="onSelectionChange" @sort-change="onSortChange">
      <el-table-column type="selection" width="50" />
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" sortable="custom" />
      <el-table-column prop="href" label="链接" min-width="220" />
      <el-table-column label="图标" width="90">
        <template #default="scope">
          <m-icon :icon="scope.row.icon" :color="scope.row.color" :size="24" />
        </template>
      </el-table-column>
      <el-table-column label="菜单" min-width="180">
        <template #default="scope">
          <el-tag v-for="m in scope.row.menus || []" :key="m.id" class="mr-1 mb-1">{{ m.title }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="order" label="排序" width="90" />
      <el-table-column label="VIP" width="80">
        <template #default="scope">
          <el-tag :type="scope.row.is_vip ? 'warning' : 'info'">{{ scope.row.is_vip ? "是" : "否" }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="scope">
          <el-tag :type="scope.row.status ? 'success' : 'danger'">{{ scope.row.status ? "启用" : "禁用" }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="scope">
          <el-button link type="primary" @click="openEdit(scope.row)">编辑</el-button>
          <el-button link type="danger" @click="onDelete(scope.row)">删除</el-button>
          <el-button link type="success" @click="onSpider(scope.row)">采集</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pager">
      <el-pagination
        v-model:current-page="pager.page"
        v-model:page-size="pager.size"
        :total="pager.total"
        background
        layout="total, sizes, prev, pager, next"
        @current-change="fetchList"
        @size-change="onSizeChange"
      />
    </div>

    <el-dialog v-model="dialog.visible" :title="dialog.isEdit ? '编辑链接' : '新增链接'" width="760px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="标题" prop="title"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="链接" prop="href"><el-input v-model="form.href" /></el-form-item>
        <el-form-item label="图标"><el-input v-model="form.icon" /></el-form-item>
        <el-form-item label="本地图标">
          <el-upload :show-file-list="false" :auto-upload="false" :on-change="onSyncCdnFile">
            <el-button>上传并同步 CDN</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="颜色"><el-color-picker v-model="form.color" /></el-form-item>
        <el-form-item label="菜单" prop="menus">
          <el-tree-select
            v-model="form.menus"
            :data="menuTree"
            multiple
            filterable
            check-strictly
            check-on-click-node
            clearable
            node-key="id"
            value-key="id"
            :props="{ label: 'title', value: 'id' }"
          />
        </el-form-item>
        <el-form-item label="站内打开"><el-switch v-model="form.is_self" /></el-form-item>
        <el-form-item label="VIP"><el-switch v-model="form.is_vip" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.status" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.order" :min="0" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.desc" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="onSubmit">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import linkModel from "@/api/links";
import menuModel from "@/api/menu";
import MIcon from "@/components/icon.vue";
import { confirmDelete, defaultPageQuery } from "@/utils/crud-helper";
import { buildOrderBy } from "@/utils/table";

const loading = ref(false);
const saving = ref(false);
const tableData = ref<any[]>([]);
const tableRef = ref<any>();
const selectedIds = ref<number[]>([]);
const menuTree = ref<any[]>([]);
const menuFlat = ref<any[]>([]);

const filters = reactive<{ title?: string; href?: string; status?: boolean; menuId?: number }>({
  title: "",
  href: "",
  status: undefined,
  menuId: undefined,
});

const pager = reactive({
  ...defaultPageQuery(),
  total: 0,
});

const dialog = reactive({ visible: false, isEdit: false, id: 0 });
const formRef = ref();
const form = reactive<any>({
  title: "",
  href: "",
  icon: "",
  color: "",
  menus: [] as number[],
  is_self: false,
  is_vip: false,
  status: true,
  order: 0,
  desc: "",
  cdn_img_id: undefined,
});

const rules = {
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  href: [{ required: true, message: "请输入链接", trigger: "blur" }],
  menus: [{ required: true, message: "请选择菜单", trigger: "change" }],
};

function flattenMenuTree(nodes: any[], result: any[] = []) {
  for (const node of nodes || []) {
    result.push({ id: node.id, title: node.title });
    if (node.children?.length) flattenMenuTree(node.children, result);
  }
  return result;
}

async function fetchMenuTree() {
  const tree = await menuModel.getMenuTree();
  menuTree.value = tree || [];
  menuFlat.value = flattenMenuTree(tree || []);
}

async function fetchList() {
  loading.value = true;
  try {
    const res = await linkModel.list(
      { page: pager.page, size: pager.size, order_by: pager.order_by },
      {
        title: filters.title || undefined,
        href: filters.href || undefined,
        status: filters.status,
        menus: filters.menuId ? [filters.menuId] : undefined,
      },
    );
    tableData.value = res.items || [];
    pager.total = res.total || 0;
  } finally {
    loading.value = false;
  }
}

function resetForm() {
  Object.assign(form, {
    title: "",
    href: "",
    icon: "",
    color: "",
    menus: [],
    is_self: false,
    is_vip: false,
    status: true,
    order: 0,
    desc: "",
    cdn_img_id: undefined,
  });
}

function onSearch() {
  pager.page = 1;
  fetchList();
}

function onReset() {
  filters.title = "";
  filters.href = "";
  filters.status = undefined;
  filters.menuId = undefined;
  onSearch();
}

function onSizeChange() {
  pager.page = 1;
  fetchList();
}

function onSortChange({ prop, order }: { prop: string; order: "ascending" | "descending" | null }) {
  pager.order_by = buildOrderBy(prop, order);
  fetchList();
}

function onSelectionChange(rows: any[]) {
  selectedIds.value = rows.map((item) => item.id);
}

function openCreate() {
  dialog.visible = true;
  dialog.isEdit = false;
  dialog.id = 0;
  resetForm();
}

function openEdit(row: any) {
  dialog.visible = true;
  dialog.isEdit = true;
  dialog.id = row.id;
  Object.assign(form, {
    title: row.title,
    href: row.href,
    icon: row.icon,
    color: row.color,
    menus: (row.menus || []).map((m: any) => m.id),
    is_self: row.is_self,
    is_vip: row.is_vip,
    status: row.status,
    order: row.order,
    desc: row.desc,
    cdn_img_id: row.cdn_img_id,
  });
}

async function onSubmit() {
  await formRef.value.validate();
  saving.value = true;
  try {
    const payload = { ...form };
    if (dialog.isEdit) {
      await linkModel.update(dialog.id, payload);
      ElMessage.success("更新成功");
    } else {
      await linkModel.create(payload);
      ElMessage.success("创建成功");
    }
    dialog.visible = false;
    await fetchList();
  } finally {
    saving.value = false;
  }
}

async function onDelete(row: any) {
  await confirmDelete("确定删除该链接吗？");
  await linkModel.delete(String(row.id));
  ElMessage.success("删除成功");
  await fetchList();
}

async function onBatchDelete() {
  if (!selectedIds.value.length) return;
  await confirmDelete(`确定批量删除 ${selectedIds.value.length} 条链接吗？`);
  await linkModel.delete(selectedIds.value.join(","));
  ElMessage.success("批量删除成功");
  selectedIds.value = [];
  tableRef.value?.clearSelection?.();
  await fetchList();
}

async function onSyncCdnFile(uploadFile: any) {
  if (!dialog.isEdit || !dialog.id) {
    ElMessage.warning("请先保存链接后再上传图标");
    return;
  }
  const file = uploadFile.raw as File;
  if (!file) return;
  const data = await linkModel.syncCdnFile(file, dialog.id);
  form.icon = data.url || form.icon;
  form.cdn_img_id = data.id;
  await linkModel.update(dialog.id, {
    icon: form.icon,
    cdn_img_id: form.cdn_img_id,
  });
  ElMessage.success("CDN 同步成功");
  await fetchList();
}

async function onSpider(row: any) {
  const data = await linkModel.getSiteInfo(row.href);
  await linkModel.update(row.id, {
    title: data.title || row.title,
    icon: data.icon || row.icon,
    desc: data.desc || row.desc,
  });
  ElMessage.success("采集成功");
  await fetchList();
}

onMounted(async () => {
  await fetchMenuTree();
  await fetchList();
});
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.pager {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
