<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import MIcon from "@/components/MIcon.vue";
import IconSelect from "@/components/icon-select/index.vue";
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
  href: "",
  icon: "",
  color: "",
  menus: [] as number[],
  order: 0,
  is_self: false,
  is_vip: false,
  status: true,
  desc: "",
};
const form = reactive({ ...defaultForm });
const spiderLoading = ref(false);
const isSpiderInfo = computed(() => isUrl(form.href));
const ruleFormRef = ref<FormInstance>();

const rules: FormRules = reactive<FormRules>({
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  icon: [{ required: true, message: "请输入图标", trigger: "blur" }],
  href: [{ required: true, message: "请输入链接", trigger: "blur" }],
  menus: [{ required: true, message: "分类必选", trigger: "blur" }],
});

async function handleSiteInfo() {
  if (!form.href) {
    ElMessage.warning("请先输入链接地址");
    return;
  }
  spiderLoading.value = true;
  linksModel
    .getSiteInfo(form.href)
    .then((data) => {
      if (data.title) form.title = data.title;
      if (data.icon) form.icon = data.icon;
      if (data.desc) form.desc = data.desc;
      ElMessage.success("抓取成功");
    })
    .finally(() => (spiderLoading.value = false));
}

function handleCancel() {
  Object.assign(form, defaultForm, { menus: [] });
  dialogFormVisible.value = false;
}

async function handleSubmit() {
  ruleFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    await linksModel.create({ ...form });
    dialogFormVisible.value = false;
    ElMessage.success("添加成功");
    Object.assign(form, defaultForm, { menus: [] });
    await menuStore.getMenuTree();
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
      append-to-body
      :close-on-click-modal="false"
      v-model="dialogFormVisible"
      :fullscreen="isMobile"
      title="添加网站"
      width="650px"
    >
      <el-form :model="form" :rules="rules" ref="ruleFormRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="链接标题" />
        </el-form-item>
        <el-form-item label="链接" prop="href">
          <div class="flex gap-2 w-full">
            <el-input v-model="form.href" placeholder="https://" />
            <el-button
              type="success"
              :disabled="!isSpiderInfo"
              :loading="spiderLoading"
              @click="handleSiteInfo"
            >抓取</el-button>
          </div>
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
        <el-form-item label="菜单" prop="menus">
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
            placeholder="选择所属菜单"
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
        <el-form-item label="站内打开" prop="is_self">
          <el-switch v-model="form.is_self" />
        </el-form-item>
        <el-form-item label="VIP" prop="is_vip">
          <el-switch v-model="form.is_vip" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch v-model="form.status" />
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input type="textarea" v-model="form.desc" placeholder="链接描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex justify-center">
          <el-button @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
