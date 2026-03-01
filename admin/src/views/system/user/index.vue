<template>
  <el-card>
    <template #header>
      <div class="toolbar">
        <el-input v-model="filters.username" placeholder="用户名" clearable @keyup.enter="onSearch" />
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
      <el-table-column prop="username" label="用户名" sortable="custom" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status ? 'success' : 'danger'">{{ scope.row.status ? "启用" : "禁用" }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
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

    <el-dialog v-model="dialog.visible" :title="dialog.isEdit ? '编辑用户' : '新增用户'" width="560px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username"><el-input v-model="form.username" :disabled="dialog.isEdit" /></el-form-item>
        <el-form-item label="密码" prop="password"><el-input v-model="form.password" show-password /></el-form-item>
        <el-form-item label="昵称" prop="nickname"><el-input v-model="form.nickname" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.status" /></el-form-item>
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
import userModel from "@/api/system/user";
import { confirmDelete, defaultPageQuery } from "@/utils/crud-helper";
import { buildOrderBy } from "@/utils/table";

const loading = ref(false);
const saving = ref(false);
const tableData = ref<any[]>([]);
const tableRef = ref<any>();
const selectedIds = ref<number[]>([]);

const filters = reactive<{ username?: string; status?: boolean }>({
  username: "",
  status: undefined,
});

const pager = reactive({
  ...defaultPageQuery(),
  total: 0,
});

const dialog = reactive({ visible: false, isEdit: false, id: 0 });
const formRef = ref();
const form = reactive({
  username: "",
  password: "",
  nickname: "",
  status: true,
});

const rules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ min: 5, max: 18, message: "密码长度应为 5-18 位", trigger: "blur" }],
};

function resetForm() {
  form.username = "";
  form.password = "";
  form.nickname = "";
  form.status = true;
}

async function fetchList() {
  loading.value = true;
  try {
    const res = await userModel.list(
      { page: pager.page, size: pager.size, order_by: pager.order_by },
      { username: filters.username || undefined, status: filters.status },
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
  filters.username = "";
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
    username: row.username,
    password: "",
    nickname: row.nickname,
    status: row.status,
  });
}

async function onSubmit() {
  await formRef.value.validate();
  saving.value = true;
  try {
    const payload: any = {
      nickname: form.nickname,
      status: form.status,
    };
    if (!dialog.isEdit) {
      payload.username = form.username;
      payload.password = form.password;
      await userModel.create(payload);
      ElMessage.success("创建成功");
    } else {
      if (form.password) payload.password = form.password;
      await userModel.update(dialog.id, payload);
      ElMessage.success("更新成功");
    }
    dialog.visible = false;
    await fetchList();
  } finally {
    saving.value = false;
  }
}

async function onDelete(row: any) {
  await confirmDelete("确定删除该用户吗？");
  await userModel.delete(String(row.id));
  ElMessage.success("删除成功");
  await fetchList();
}

async function onBatchDelete() {
  if (!selectedIds.value.length) return;
  await confirmDelete(`确定批量删除 ${selectedIds.value.length} 个用户吗？`);
  await userModel.delete(selectedIds.value.join(","));
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
