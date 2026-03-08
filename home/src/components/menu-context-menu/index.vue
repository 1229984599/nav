<script setup lang="ts">
import { reactive, ref, nextTick } from "vue";
import MIcon from "@/components/MIcon.vue";
import IconSelect from "@/components/icon-select/index.vue";
import menuApi from "@/api/menu";
import { isMobile } from "@/utils/window";
import { ElMessage, ElMessageBox, type FormInstance, FormRules } from "element-plus";
import { useMenuStore } from "@/store/menu";
import { MenuSchemaTree } from "@/api/menu/types";

defineOptions({
  name: "MMenuContextMenu",
});

const menuStore = useMenuStore();

// 右键菜单状态
const menuVisible = ref(false);
const menuStyle = reactive({ left: "0px", top: "0px" });
const currentItem = ref<MenuSchemaTree | null>(null);

// 编辑弹窗状态
const dialogVisible = ref(false);
const editLoading = ref(false);
const ruleFormRef = ref<FormInstance>();

const form = reactive({
  title: "",
  icon: "",
  color: "",
  parent_id: null as number | null,
  order: 0,
  is_vip: false,
  status: true,
});

const rules: FormRules = reactive<FormRules>({
  title: [{ required: true, message: "请输入分类名称", trigger: "blur" }],
  icon: [{ required: true, message: "请输入图标", trigger: "blur" }],
});

function show(event: MouseEvent | TouchEvent, item: MenuSchemaTree) {
  if (event instanceof MouseEvent) {
    event.preventDefault();
    event.stopPropagation();
    menuStyle.left = event.clientX + "px";
    menuStyle.top = event.clientY + "px";
  } else if (event instanceof TouchEvent && event.touches.length > 0) {
    event.preventDefault();
    event.stopPropagation();
    menuStyle.left = event.touches[0].clientX + "px";
    menuStyle.top = event.touches[0].clientY + "px";
  }
  currentItem.value = item;
  menuVisible.value = true;

  const hide = () => {
    menuVisible.value = false;
    document.removeEventListener("click", hide);
    document.removeEventListener("contextmenu", hide);
    document.removeEventListener("touchstart", hide);
  };
  nextTick(() => {
    document.addEventListener("click", hide);
    document.addEventListener("contextmenu", hide);
    document.addEventListener("touchstart", hide);
  });
}

async function handleEdit() {
  menuVisible.value = false;
  if (!currentItem.value?.id) return;
  editLoading.value = true;
  try {
    const item = await menuApi.read(currentItem.value.id);
    form.title = item.title || "";
    form.icon = item.icon || "";
    form.color = item.color || "";
    form.parent_id = item.parent_id ?? null;
    form.order = item.order ?? 0;
    form.is_vip = item.is_vip || false;
    form.status = item.status ?? true;
    dialogVisible.value = true;
  } catch (e) {
    console.error("获取分类详情失败", e);
  } finally {
    editLoading.value = false;
  }
}

function handleDelete() {
  menuVisible.value = false;
  if (!currentItem.value?.id) return;
  const id = currentItem.value.id;
  const title = currentItem.value.title || "";
  ElMessageBox.confirm(`确定删除分类「${title}」吗？该分类下的链接不会被删除。`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await menuApi.delete(String(id));
      ElMessage.success("删除成功");
      await menuStore.getMenuTree();
    })
    .catch(() => {});
}

async function handleSubmit() {
  ruleFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    if (!currentItem.value?.id) return;
    await menuApi.update(currentItem.value.id, { ...form });
    dialogVisible.value = false;
    ElMessage.success("修改成功");
    await menuStore.getMenuTree();
  });
}

function handleCancel() {
  dialogVisible.value = false;
}

defineExpose({ show });
</script>

<template>
  <!-- 右键菜单 -->
  <teleport to="body">
    <div
      v-show="menuVisible"
      class="context-menu"
      :style="menuStyle"
    >
      <div class="context-menu-item" @click="handleEdit">
        <m-icon icon="mdi:pencil-outline" :size="16" />
        <span>编辑</span>
      </div>
      <div class="context-menu-item context-menu-item--danger" @click="handleDelete">
        <m-icon icon="mdi:delete-outline" :size="16" />
        <span>删除</span>
      </div>
    </div>
  </teleport>

  <!-- 编辑弹窗 -->
  <el-dialog
    center
    append-to-body
    :close-on-click-modal="false"
    v-model="dialogVisible"
    :fullscreen="isMobile"
    title="编辑分类"
    width="500px"
  >
    <el-form v-loading="editLoading" :model="form" :rules="rules" ref="ruleFormRef" label-width="80px">
      <el-form-item label="名称" prop="title">
        <el-input v-model="form.title" placeholder="分类名称" />
      </el-form-item>
      <el-form-item label="图标" prop="icon">
        <icon-select v-model="form.icon" :color="form.color" />
      </el-form-item>
      <el-form-item label="颜色" prop="color">
        <el-color-picker
          size="large"
          v-model="form.color"
          :predefine="[
            '#ff4500',
            '#ff8c00',
            '#ffd700',
            '#90ee90',
            '#00ced1',
            '#1e90ff',
            '#c71585',
            '#c7158577',
          ]"
        />
      </el-form-item>
      <el-form-item label="父分类">
        <el-tree-select
          v-model="form.parent_id"
          :data="menuStore.menuTree"
          :render-after-expand="false"
          highlight-current
          filterable
          clearable
          check-on-click-node
          placeholder="无（顶级分类）"
          class="w-full"
          :props="{
            label: 'title',
            value: 'id',
          }"
          node-key="id"
          value-key="id"
        >
          <template #default="{ data }">
            <div class="flex gap-x-1">
              <m-icon :size="20" :color="data.color" :icon="data?.icon" />
              <span>{{ data.title }}</span>
            </div>
          </template>
        </el-tree-select>
      </el-form-item>
      <el-form-item label="排序" prop="order">
        <el-input-number v-model="form.order" :min="0" />
      </el-form-item>
      <el-form-item label="VIP" prop="is_vip">
        <el-switch v-model="form.is_vip" />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-switch v-model="form.status" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="flex justify-center">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.context-menu {
  position: fixed;
  z-index: 9999;
  background: var(--nav-card-bg, #fff);
  border: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));
  border-radius: 6px;
  padding: 4px 0;
  min-width: 120px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.context-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  color: var(--nav-text, #1f2937);
  transition: background-color 0.15s;

  &:hover {
    background-color: rgba(0, 0, 0, 0.04);
  }

  &--danger {
    color: #ef4444;

    &:hover {
      background-color: rgba(239, 68, 68, 0.08);
    }
  }
}
</style>
