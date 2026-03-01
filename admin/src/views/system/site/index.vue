<template>
  <el-card class="site-card">
    <el-form ref="formRef" :model="form" :rules="rules" label-width="110px" v-loading="loading">
      <el-form-item label="站点名称" prop="title"><el-input v-model="form.title" /></el-form-item>
      <el-form-item label="关键词"><el-input v-model="form.keywords" /></el-form-item>
      <el-form-item label="描述"><el-input v-model="form.desc" type="textarea" :rows="3" /></el-form-item>
      <el-form-item label="图标"><el-input v-model="form.icon" /></el-form-item>
      <el-form-item label="颜色"><el-color-picker v-model="form.color" /></el-form-item>
      <el-form-item label="开启一言"><el-switch v-model="form.yiyan" /></el-form-item>
      <el-form-item label="开启天气"><el-switch v-model="form.weather" /></el-form-item>
      <el-form-item label="天气 Key" v-if="form.weather"><el-input v-model="form.weather_key" /></el-form-item>
      <el-form-item label="图床 Token"><el-input v-model="form.cdn_img_token" /></el-form-item>
      <el-form-item label="备案号"><el-input v-model="form.copyright" /></el-form-item>
      <el-form-item label="尾部信息"><el-input v-model="form.footer" type="textarea" :rows="3" /></el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="saving" @click="onSubmit">保存</el-button>
        <el-button @click="onClearCache">清理缓存</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import siteModel from "@/api/site";

const loading = ref(false);
const saving = ref(false);
const formRef = ref();

const form = reactive<any>({
  id: undefined,
  title: "",
  keywords: "",
  desc: "",
  icon: "",
  color: "",
  yiyan: false,
  weather: false,
  weather_key: "",
  cdn_img_token: "",
  copyright: "",
  footer: "",
  status: true,
});

const rules = {
  title: [{ required: true, message: "请输入站点名称", trigger: "blur" }],
};

async function fetchSite() {
  loading.value = true;
  try {
    const data = await siteModel.get();
    Object.assign(form, data || {});
  } finally {
    loading.value = false;
  }
}

async function onSubmit() {
  await formRef.value.validate();
  saving.value = true;
  try {
    await siteModel.update({ ...form });
    ElMessage.success("保存成功");
    await fetchSite();
  } finally {
    saving.value = false;
  }
}

async function onClearCache() {
  await siteModel.clearCache();
  ElMessage.success("缓存已清理");
}

onMounted(fetchSite);
</script>

<style scoped>
.site-card {
  max-width: 900px;
}
</style>

