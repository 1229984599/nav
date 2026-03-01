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
      </div>
    </template>

    <el-table :data="tableData" v-loading="loading" row-key="id" default-expand-all>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
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

    <el-dialog v-model="dialog.visible" :title="dialog.isEdit ? '编辑菜单' : '新增菜单'" width="620px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="标题" prop="title"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="图标"><el-input v-model="form.icon" /></el-form-item>
        <el-form-item label="颜色"><el-color-picker v-model="form.color" /></el-form-item>
        <el-form-item label="父级菜单">
          <el-select v-model="form.parent_id" placeholder="可选" clearable>
            <el-option :value="0" label="顶级菜单" />
            <el-option v-for="item in topMenus" :key="item.id" :value="item.id" :label="item.title" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.order" :min="0" /></el-form-item>
        <el-form-item label="VIP"><el-switch v-model="form.is_vip" /></el-form-item>
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
import menuModel from "@/api/menu";
import MIcon from "@/components/icon.vue";
import { confirmDelete } from "@/utils/crud-helper";

const loading = ref(false);
const saving = ref(false);
const tableData = ref<any[]>([]);
const sourceTree = ref<any[]>([]);
const topMenus = ref<any[]>([]);

const filters = reactive<{ title?: string; status?: boolean }>({
  title: "",
  status: undefined,
});

const dialog = reactive({ visible: false, isEdit: false, id: 0 });
const formRef = ref();
const form = reactive<any>({
  title: "",
  icon: "",
  color: "",
  parent_id: 0,
  order: 0,
  is_vip: false,
  status: true,
});

const rules = {
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
};

function filterTree(nodes: any[], title?: string, status?: boolean) {
  return (nodes || [])
    .map((node: any) => {
      const children = filterTree(node.children || [], title, status);
      const hitTitle = !title || node.title?.includes(title);
      const hitStatus = status === undefined || node.status === status;
      if ((hitTitle && hitStatus) || children.length) {
        return { ...node, children };
      }
      return null;
    })
    .filter(Boolean);
}

async function fetchTree() {
  loading.value = true;
  try {
    const data = await menuModel.getMenuTree();
    sourceTree.value = data || [];
    tableData.value = sourceTree.value;
    topMenus.value = (sourceTree.value || []).map((x: any) => ({ id: x.id, title: x.title }));
  } finally {
    loading.value = false;
  }
}

function onSearch() {
  tableData.value = filterTree(sourceTree.value, filters.title || undefined, filters.status);
}

function onReset() {
  filters.title = "";
  filters.status = undefined;
  tableData.value = sourceTree.value;
}

function resetForm() {
  Object.assign(form, {
    title: "",
    icon: "",
    color: "",
    parent_id: 0,
    order: 0,
    is_vip: false,
    status: true,
  });
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
    icon: row.icon,
    color: row.color,
    parent_id: row.parent_id || 0,
    order: row.order,
    is_vip: row.is_vip,
    status: row.status,
  });
}

async function onSubmit() {
  await formRef.value.validate();
  saving.value = true;
  try {
    const payload = { ...form };
    if (dialog.isEdit) {
      await menuModel.update(dialog.id, payload);
      ElMessage.success("更新成功");
    } else {
      await menuModel.create(payload);
      ElMessage.success("创建成功");
    }
    dialog.visible = false;
    await fetchTree();
  } finally {
    saving.value = false;
  }
}

async function onDelete(row: any) {
  await confirmDelete("确定删除该菜单吗？");
  await menuModel.delete(String(row.id));
  ElMessage.success("删除成功");
  await fetchTree();
}

onMounted(fetchTree);
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}
</style>

