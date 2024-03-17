<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import MIcon from "@/components/MIcon.vue";
import linksModel from "@/api/links";
import { isMobile, isUrl } from "@/utils/window";
import { ElMessage, type FormInstance, FormRules } from "element-plus";
import { useMenuStore } from "@/store/menu";

defineOptions({
  name: "MAddLink",
});

const dialogFormVisible = ref(false);
const menuStore = useMenuStore();
const defaultForm = {
  title: "",
  icon: "",
  href: "",
  desc: "",
  color: "",
  is_self: false,
  menus: [],
};
const form = reactive({
  title: "",
  icon: "",
  href: "",
  desc: "",
  color: "",
  is_self: false,
  menus: [],
});
const spiderLoading = ref(false);
const isSpiderInfo = computed(() => {
  return isUrl(form.href);
});
const ruleFormRef = ref<FormInstance>();

const rules: FormRules = reactive<FormRules>({
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  icon: [{ required: true, message: "请输入图标", trigger: "blur" }],
  href: [{ required: true, message: "请输入链接", trigger: "blur" }],
  menus: [{ required: true, message: "分类必选", trigger: "blur" }],
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
  Object.assign(form, defaultForm);
  dialogFormVisible.value = false;
}

/**
 * 处理提交数据
 */
async function handleSubmit() {
  ruleFormRef.value?.validate((valid: boolean) => {
    if (!valid) return;
    linksModel.create(form).then(() => {
      dialogFormVisible.value = false;
      ElMessage.success("添加成功");
      Object.assign(form, defaultForm);
      location.reload();
    });
  });
}
</script>

<template>
  <div>
    <m-icon
      @click="dialogFormVisible = true"
      class="hover:text-red-900"
      icon="gridicons:add-outline"
    />

    <el-dialog
      center
      :close-on-click-modal="false"
      v-model="dialogFormVisible"
      :fullscreen="isMobile"
      title="添加网站"
    >
      <el-form :model="form" :rules="rules" ref="ruleFormRef">
        <el-form-item label="链接" prop="href">
          <el-input v-model="form.href" />
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="form.icon">
            <template #append>
              <m-icon :color="form.color" :icon="form.icon" />
            </template>
          </el-input>
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
          ></el-color-picker>
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input type="textarea" v-model="form.desc" />
        </el-form-item>
        <el-form-item label="分类" prop="menus">
          <el-tree-select
            v-model="form.menus"
            :data="menuStore.menuTree"
            multiple
            :render-after-expand="false"
            show-checkbox
            check-strictly
            highlight-current
            filterable
            clearable
            check-on-click-node
            placeholder="请选择"
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
          <el-button type="primary" @click="handleSubmit">确定</el-button>
          <el-button type="danger" @click="handleCancel">取消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-input-group__append) {
  //border-color: transparent;
  box-shadow: none;
  color: unset;
  background-color: white;
}
</style>
