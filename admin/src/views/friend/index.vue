<template>
  <el-card>
    <template #header>
      <div class="toolbar">
        <el-input v-model="filters.title" placeholder="标题" clearable @keyup.enter="onSearch" />
        <el-select v-model="filters.status" placeholder="状态" clearable>
          <el-option :value="true" label="启用" />
          <el-option :value="false" label="禁用" />
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
      <el-table-column prop="href" label="链接" />
      <el-table-column label="图标" width="90">
        <template #default="scope">
          <m-icon :icon="scope.row.icon" :color="scope.row.color" :size="24" />
        </template>
      </el-table-column>
      <el-table-column prop="order" label="排序" width="90" />
      <el-table-column label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status ? 'success' : 'danger'">{{ scope.row.status ? "启用" : "禁用" }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button link type="primary" @click="openEdit(scope.row)">编辑</el-button>
          <el-button link type="danger" @click="onDelete(scope.row)">删除</el-button>
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

    <el-dialog v-model="dialog.visible" :title="dialog.isEdit ? '编辑友链' : '新增友链'" width="640px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="链接" prop="href"><el-input v-model="form.href" /></el-form-item>
        <el-form-item label="图标"><el-input v-model="form.icon" /></el-form-item>
        <el-form-item label="颜色"><el-color-picker v-model="form.color" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.order" :min="0" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.status" /></el-form-item>
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
import { reactive, ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import friendModel from "@/api/friend";
import MIcon from "@/components/icon.vue";
import { confirmDelete, defaultPageQuery } from "@/utils/crud-helper";
import { buildOrderBy } from "@/utils/table";

const loading = ref(false);
const saving = ref(false);
const tableData = ref<any[]>([]);
const tableRef = ref<any>();
const selectedIds = ref<number[]>([]);

const filters = reactive<{ title?: string; status?: boolean }>({
  title: "",
  status: undefined,
});

const pager = reactive({
  ...defaultPageQuery(),
  total: 0,
});

const dialog = reactive({ visible: false, isEdit: false, id: 0 });
const formRef = ref();
const form = reactive({
  title: "",
  href: "",
  icon: "",
  color: "",
  order: 0,
  status: true,
  desc: "",
});

const rules = {
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  href: [{ required: true, message: "请输入链接", trigger: "blur" }],
};

function resetForm() {
  form.title = "";
  form.href = "";
  form.icon = "";
  form.color = "";
  form.order = 0;
  form.status = true;
  form.desc = "";
}

async function fetchList() {
  loading.value = true;
  try {
    const res = await friendModel.list(
      { page: pager.page, size: pager.size, order_by: pager.order_by },
      { title: filters.title || undefined, status: filters.status },
    );
    tableData.value = res.items || [];
    pager.total = res.total || 0;
  } finally {
    loading.value = false;
  }
}

function onSearch() {
  pager.page = 1;
  fetchList();
}

function onReset() {
  filters.title = "";
  filters.status = undefined;
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
    order: row.order,
    status: row.status,
    desc: row.desc,
  });
}

async function onSubmit() {
  await formRef.value.validate();
  saving.value = true;
  try {
    const payload = { ...form };
    if (dialog.isEdit) {
      await friendModel.update(dialog.id, payload);
      ElMessage.success("更新成功");
    } else {
      await friendModel.create(payload);
      ElMessage.success("创建成功");
    }
    dialog.visible = false;
    await fetchList();
  } finally {
    saving.value = false;
  }
}

async function onDelete(row: any) {
  await confirmDelete("确定删除该友链吗？");
  await friendModel.delete(String(row.id));
  ElMessage.success("删除成功");
  await fetchList();
}

async function onBatchDelete() {
  if (!selectedIds.value.length) return;
  await confirmDelete(`确定批量删除 ${selectedIds.value.length} 条友链吗？`);
  await friendModel.delete(selectedIds.value.join(","));
  ElMessage.success("批量删除成功");
  selectedIds.value = [];
  tableRef.value?.clearSelection?.();
  await fetchList();
}

onMounted(fetchList);
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
