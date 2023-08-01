<script lang="ts" setup>
import { onMounted, reactive, ref } from "vue";
import { SiteSchema } from "@/api/site/types";
import siteModel from "@/api/site";
import MIcon from "@/components/MIcon.vue";
import { ElMessage, FormInstance, FormRules } from "element-plus";

const form = reactive<SiteSchema>({
  id: null,
  title: "",
  keywords: "",
  desc: "",
  icon: "",
  color: "",
  footer: ""
});
const ruleFormRef = ref<FormInstance>();

const rules: FormRules = reactive<FormRules>({
  // title: [{ required: true, message: "请输入标题", trigger: "blur" }]
  // icon: [{ required: true, message: "请输入图标", trigger: "blur" }],
  // href: [{ required: true, message: "请输入链接", trigger: "blur" }],
  // desc: [{ required: true, message: "请输入描述", trigger: "blur" }],
});
function handleSubmit() {
  ruleFormRef.value?.validate((valid: boolean) => {
    if (!valid) return;
    siteModel.update(form).then(data => {
      ElMessage.success("保存成功");
      Object.assign(form, data);
      // location.reload();
    });
  });
}

onMounted(async () => {
  const data = await siteModel.get();
  Object.assign(form, data);
  debugger;
});
</script>
<template>
  <div class="p-4 bg-white w-2/3">
    <el-form :model="form" :rules="rules" ref="ruleFormRef">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="关键词" prop="keywords">
        <el-input v-model="form.keywords" />
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input type="textarea" v-model="form.desc" />
      </el-form-item>
      <el-form-item label="尾部" prop="footer">
        <el-input type="textarea" v-model="form.footer" />
      </el-form-item>
      <el-form-item label="图标" prop="icon">
        <el-input v-model="form.icon">
          <template #append>
            <m-icon :color="form.color" :icon="form.icon" />
          </template>
        </el-input>
        <span class="text-gray-400 text-sm"
          ><a href="https://icon-sets.iconify.design/" target="_blank">
            点我前往iconify查看图标
          </a></span
        >
      </el-form-item>
      <el-form-item label="颜色" prop="color">
        <el-color-picker
          v-model="form.color"
          :predefine="[
            '#ff4500',
            '#ff8c00',
            '#ffd700',
            '#90ee90',
            '#00ced1',
            '#1e90ff',
            '#c71585',
            '#c7158577'
          ]"
        ></el-color-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
        <el-button type="danger">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
