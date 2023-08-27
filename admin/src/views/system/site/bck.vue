<script lang="ts" setup>
import { onBeforeMount, onMounted, onUnmounted, onUpdated, ref } from "vue";
import { useColumns } from "@fast-crud/fast-crud";
import { FormScopeContext } from "@fast-crud/fast-crud/dist/d/d/crud";
import { UseIconForm } from "@/hooks/icon";
import siteModel from "@/api/site";

const formRef = ref();
const formOptions = ref();
const { buildFormOptions } = useColumns();
const iconForm = UseIconForm();
formOptions.value = buildFormOptions({
  form: {
    col: {
      span: 24,
    },
    doSubmit: ({ form }: FormScopeContext) => {
      console.log(form);
    },
  },
  columns: {
    title: {
      title: "站点名称",
      type: "text",
      form: {
        rules: [{ required: true, message: "此项必填" }],
      },
    },
    keywords: {
      title: "关键词",
      type: "text",
    },
    desc: {
      title: "描述",
      type: "textarea",
    },
    ...iconForm,
    footer: {
      title: "尾部信息",
      type: "textarea",
    },
  },
});
onMounted(async () => {
  // debugger;
  const data = await siteModel.get();
  Object.assign(formOptions.value.initialForm, data);
});
</script>
<template>
  <div class="h-full mt-3 p-2 w-2/3">
    <fs-form ref="formRef" v-bind="formOptions" />
    <div style="margin-top: 10px">
      <el-button>提交表单</el-button>
      <el-button>重置表单</el-button>
    </div>
  </div>
</template>
