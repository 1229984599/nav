<script lang="tsx" setup>
import { nextTick, ref } from "vue";
import { compute, dict, useColumns } from "@fast-crud/fast-crud";
import { FormScopeContext } from "@fast-crud/fast-crud/dist/d/d/crud";
import { UseIconForm } from "@/hooks/icon";
import siteModel from "@/api/site";
import { ElMessage } from "element-plus";
import { isMobile } from "@/utils/window";

const formRef = ref();
const formOptions = ref();
const { buildFormOptions } = useColumns();
const iconForm = UseIconForm(siteModel, false);
const submitLoading = ref(false);
formOptions.value = buildFormOptions({
  form: {
    col: {
      span: 24,
    },
    doSubmit: ({ form }: FormScopeContext) => {
      submitLoading.value = true;
      siteModel
        .update(form)
        .then(() => {
          ElMessage.success("修改成功");
        })
        .finally(() => (submitLoading.value = false));
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
    yiyan: {
      title: "开启一言",
      type: "dict-switch",
      form: {
        col: { span: isMobile.value ? 24 : 6 },
      },
      dict: dict({
        data: [
          { value: true, label: "是" },
          { value: false, label: "否" },
        ],
      }),
    },
    weather: {
      title: "开启天气",
      type: "dict-switch",
      form: {
        col: { span: isMobile.value ? 24 : 6 },
      },
      dict: dict({
        data: [
          { value: true, label: "是" },
          { value: false, label: "否" },
        ],
      }),
    },
    weather_key: {
      title: "天气key",
      type: "text",
      form: {
        show: compute((context) => {
          return context.form.weather;
        }),
        helper: {
          render: () => {
            return (
              <a href="https://console.qweather.com/#/apps" target="_blank">
                点我前往和风天气获取开发者key
              </a>
            );
          },
        },
      },
    },
    cdn_img_token: {
      title: "图床token",
      type: "text",
      form: {
        helper: {
          render: () => {
            return (
              <a href="https://img.ink/user/settings.html" target="_blank">
                点我前往水墨图床获取token
              </a>
            );
          },
        },
      },
    },
    ...iconForm,
    copyright: {
      title: "备案号",
      type: "text",
    },
    footer: {
      title: "尾部信息",
      type: "textarea",
    },
  },
});
// nextTick
nextTick(async () => {
  // debugger;
  const data = await siteModel.get();
  Object.assign(formRef.value.form, data);
});

function reset() {
  formRef.value.reset();
}

function handleSubmit() {
  formRef.value.submit();
}
</script>
<template>
  <fs-page class="h-full mt-3 p-2 w-2/3">
    <fs-form ref="formRef" v-bind="formOptions" />
    <div style="margin-top: 10px">
      <el-button :loading="submitLoading" type="primary" @click="handleSubmit"
        >修改数据
      </el-button>
      <!--        <el-button @click="reset">重置表单</el-button>-->
    </div>
  </fs-page>
</template>
