<script setup lang="ts">
import { reactive, ref, computed } from "vue";
import MIconSelect from "@/components/icon-select/index.vue";
import { useBookmarkStore } from "@/store/bookmark";
import { DEFAULT_GROUP_ID } from "@/types/bookmark";
import type { BookmarkGroup } from "@/types/bookmark";
import type { FormInstance, FormRules } from "element-plus";

defineOptions({ name: "BookmarkGroupDialog" });

const bookmarkStore = useBookmarkStore();
const dialogVisible = defineModel<boolean>();
const formRef = ref<FormInstance>();

const isEdit = ref(false);
const editingId = ref("");

const form = reactive({
  name: "",
  icon: "mdi:folder",
  color: "#409eff",
});

const rules: FormRules = {
  name: [{ required: true, message: "请输入分组名称", trigger: "blur" }],
};

const predefineColors = [
  "#ff4500", "#ff8c00", "#ffd700", "#90ee90",
  "#00ced1", "#1e90ff", "#c71585", "#409eff",
];

function open(group?: BookmarkGroup) {
  if (group && group.id !== DEFAULT_GROUP_ID) {
    isEdit.value = true;
    editingId.value = group.id;
    form.name = group.name;
    form.icon = group.icon;
    form.color = group.color;
  } else {
    isEdit.value = false;
    editingId.value = "";
    form.name = "";
    form.icon = "mdi:folder";
    form.color = "#409eff";
  }
  dialogVisible.value = true;
}

const canDelete = computed(() => {
  return isEdit.value && editingId.value !== DEFAULT_GROUP_ID;
});

async function handleSubmit() {
  await formRef.value?.validate();
  if (isEdit.value) {
    bookmarkStore.updateGroup(editingId.value, {
      name: form.name,
      icon: form.icon,
      color: form.color,
    });
  } else {
    bookmarkStore.addGroup({
      name: form.name,
      icon: form.icon,
      color: form.color,
    });
  }
  dialogVisible.value = false;
}

function handleDelete() {
  if (!canDelete.value) return;
  bookmarkStore.deleteGroup(editingId.value);
  dialogVisible.value = false;
}

defineExpose({ open });
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑分组' : '新建分组'"
    width="420px"
    center
    :close-on-click-modal="false"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="70px">
      <el-form-item label="名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入分组名称" />
      </el-form-item>
      <el-form-item label="图标" prop="icon">
        <m-icon-select v-model="form.icon" :color="form.color" />
      </el-form-item>
      <el-form-item label="颜色" prop="color">
        <el-color-picker
          v-model="form.color"
          size="large"
          :predefine="predefineColors"
          @active-change="(c: string) => (form.color = c)"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="flex justify-between">
        <div>
          <el-popconfirm
            v-if="canDelete"
            title="删除分组后，其下书签将移至未分类，确定？"
            confirm-button-text="删除"
            cancel-button-text="取消"
            @confirm="handleDelete"
          >
            <template #reference>
              <el-button type="danger" plain>删除分组</el-button>
            </template>
          </el-popconfirm>
        </div>
        <div>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>
