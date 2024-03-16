<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import MIcon from "@/components/MIcon.vue";
import linksModel from "@/api/links";
import { isMobile, isUrl } from "@/utils/window";
import { ElMessage, type FormInstance, FormRules } from "element-plus";
import { useMenuStore } from "@/store/menu";
import { cloneDeep } from "lodash-es";

defineOptions({
  name: "MLocalAddLink",
});

const menuStore = useMenuStore();
const dialogFormVisible = defineModel();

const form = reactive({
  title: "",
  icon: "",
  href: "",
  desc: "",
  color: "",
  status: true,
  is_self: false,
});
const spiderLoading = ref(false);
const isSpiderInfo = computed(() => {
  return isUrl(form.href);
});
const ruleFormRef = ref<FormInstance>();

const rules: FormRules = reactive<FormRules>({
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  // icon: [{ required: true, message: "请输入图标", trigger: "blur" }],
  href: [{ required: true, message: "请输入链接", trigger: "blur" }],
});

/**
 * 根据url采集站点信息
 */
async function handleSiteInfo() {
  spiderLoading.value = true;
  linksModel
    .getSiteInfo(form.href)
    .then((data) => {
      Object.assign(form, data);
    })
    .finally(() => (spiderLoading.value = false));
}

function handleCancel() {
  ruleFormRef.value?.resetFields();
  dialogFormVisible.value = false;
}

/**
 * 处理提交数据
 */
async function handleSubmit() {
  ruleFormRef.value?.validate((valid: boolean) => {
    if (!valid) return;
    // 处理添加链接
    menuStore.addLocalLink(cloneDeep(form));
    ElMessage.success("操作成功");
    ruleFormRef.value?.resetFields();
    dialogFormVisible.value = false;
  });
}

function handleReset() {
  ruleFormRef.value?.resetFields();
}

defineExpose({ form, formRef: ruleFormRef.value });
</script>

<template>
  <el-dialog
    center
    :close-on-click-modal="false"
    v-model="dialogFormVisible"
    :fullscreen="isMobile"
    title="网站信息"
  >
    <el-form :model="form" :rules="rules" ref="ruleFormRef">
      <el-form-item label="链接" prop="href">
        <el-input placeholder="请输入链接" v-model="form.href" />
      </el-form-item>
      <el-form-item label="标题" prop="title">
        <el-input placeholder="请输入标题" v-model="form.title" />
      </el-form-item>
      <el-form-item label="图标" prop="icon">
        <el-input placeholder="请输入图标" v-model="form.icon">
          <template #append>
            <m-icon :color="form.color" :icon="form.icon" />
          </template>
          <template #suffix>
            <a
              href="https://icon-sets.iconify.design/?query=logo"
              target="_blank"
              >查看图标
            </a>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item label="颜色" prop="color">
        <el-color-picker
          size="large"
          v-model="form.color"
          @active-change="
            (color: string) => {
              form.color = color;
            }
          "
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
        ></el-color-picker>
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

<style lang="scss" scoped>
:deep(.el-input-group__append) {
  //border-color: transparent;
  box-shadow: none;
  color: unset;
  background-color: white;
}
</style>
