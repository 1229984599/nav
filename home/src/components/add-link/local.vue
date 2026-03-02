<script setup lang="ts">
import { computed, nextTick, reactive, ref } from "vue";
import MIconSelect from "@/components/icon-select/index.vue";
import linksModel from "@/api/links";
import { isUrl } from "@/utils/window";
import { isMobile } from "@/utils/window";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";
import { useBookmarkStore } from "@/store/bookmark";
import { DEFAULT_GROUP_ID } from "@/types/bookmark";

defineOptions({ name: "MLocalAddLink" });

const bookmarkStore = useBookmarkStore();
const dialogFormVisible = defineModel<boolean>();

const editingId = ref("");

const form = reactive({
  title: "",
  icon: "",
  href: "",
  desc: "",
  color: "",
  is_self: false,
  groupIds: [DEFAULT_GROUP_ID] as string[],
});

const spiderLoading = ref(false);
const isSpiderInfo = computed(() => isUrl(form.href));
const ruleFormRef = ref<FormInstance>();

const rules: FormRules = reactive<FormRules>({
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  href: [{ required: true, message: "请输入链接", trigger: "blur" }],
});

/** 根据url采集站点信息 */
async function handleSiteInfo() {
  spiderLoading.value = true;
  linksModel
    .getSiteInfo(form.href)
    .then((data: any) => {
      if (data.title) form.title = data.title;
      if (data.icon) form.icon = data.icon;
      if (data.desc) form.desc = data.desc;
      if (data.color) form.color = data.color;
    })
    .finally(() => (spiderLoading.value = false));
}

/** 粘贴URL时自动采集 */
function onHrefPaste() {
  nextTick(() => {
    if (isSpiderInfo.value && !form.title) {
      handleSiteInfo();
    }
  });
}

function handleCancel() {
  ruleFormRef.value?.resetFields();
  editingId.value = "";
  dialogFormVisible.value = false;
}

/** 提交数据 */
async function handleSubmit() {
  ruleFormRef.value?.validate((valid: boolean) => {
    if (!valid) return;
    if (editingId.value) {
      bookmarkStore.updateLink(editingId.value, {
        href: form.href,
        title: form.title,
        icon: form.icon,
        color: form.color,
        desc: form.desc,
        is_self: form.is_self,
        groupIds: form.groupIds.length > 0 ? form.groupIds : [DEFAULT_GROUP_ID],
      });
    } else {
      bookmarkStore.addLink({
        href: form.href,
        title: form.title,
        icon: form.icon,
        color: form.color,
        desc: form.desc,
        is_self: form.is_self,
        groupIds: form.groupIds.length > 0 ? form.groupIds : [DEFAULT_GROUP_ID],
      });
    }
    ElMessage.success("操作成功");
    ruleFormRef.value?.resetFields();
    editingId.value = "";
    dialogFormVisible.value = false;
  });
}

function handleReset() {
  ruleFormRef.value?.resetFields();
}

function setEditData(data: any) {
  editingId.value = data.id || "";
  form.href = data.href || "";
  form.title = data.title || "";
  form.icon = data.icon || "";
  form.color = data.color || "";
  form.desc = data.desc || "";
  form.is_self = data.is_self || false;
  form.groupIds = data.groupIds && data.groupIds.length > 0
    ? [...data.groupIds]
    : data.groupId
      ? [data.groupId]
      : [DEFAULT_GROUP_ID];
}

defineExpose({ form, formRef: ruleFormRef, setEditData });
</script>

<template>
  <el-dialog
    center
    :close-on-click-modal="false"
    v-model="dialogFormVisible"
    :fullscreen="isMobile"
    :title="editingId ? '编辑书签' : '添加书签'"
    width="500px"
  >
    <el-form :model="form" :rules="rules" ref="ruleFormRef" label-width="80px">
      <el-form-item label="链接" prop="href">
        <el-input
          placeholder="请输入链接"
          v-model="form.href"
          @paste="onHrefPaste"
        />
      </el-form-item>
      <el-form-item label="标题" prop="title">
        <el-input placeholder="请输入标题" v-model="form.title" />
      </el-form-item>
      <el-form-item label="图标" prop="icon">
        <m-icon-select v-model="form.icon" :color="form.color" />
      </el-form-item>
      <el-form-item label="颜色" prop="color">
        <el-color-picker
          size="large"
          v-model="form.color"
          @active-change="(color: string) => (form.color = color)"
          :predefine="[
            '#ff4500', '#ff8c00', '#ffd700', '#90ee90',
            '#00ced1', '#1e90ff', '#c71585', '#c7158577',
          ]"
        />
      </el-form-item>
      <el-form-item label="分组" prop="groupIds">
        <el-select v-model="form.groupIds" placeholder="选择分组" multiple collapse-tags collapse-tags-tooltip>
          <el-option
            v-for="g in bookmarkStore.sortedGroups"
            :key="g.id"
            :label="g.name"
            :value="g.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input
          placeholder="请输入描述"
          type="textarea"
          v-model="form.desc"
        />
      </el-form-item>
      <el-form-item label="站内打开" prop="is_self">
        <el-switch
          v-model="form.is_self"
          active-text="是"
          inactive-text="否"
          inline-prompt
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="flex justify-center">
        <el-button
          :disabled="!isSpiderInfo"
          :loading="spiderLoading"
          type="success"
          @click="handleSiteInfo"
          >采集
        </el-button>
        <el-button type="warning" @click="handleReset">重置</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
        <el-button type="danger" @click="handleCancel">取消</el-button>
      </div>
    </template>
  </el-dialog>
</template>
