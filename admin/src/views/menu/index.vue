<template>
  <fs-page>
    <fs-crud ref="crudRef" v-bind="crudBinding" />
  </fs-page>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useCrud, useExpose } from "@fast-crud/fast-crud";
import createCrudOptions from "./crud";

// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置
const { crudOptions } = createCrudOptions(crudExpose);
// eslint-disable-next-line @typescript-eslint/no-unused-vars,no-unused-vars
// 初始化crud配置
// 此处传入权限前缀进行通用按钮权限设置，会通过commonOptions去设置actionbar和rowHandle的按钮的show属性
// 更多关于按钮权限的源代码设置，请参考 ./src/plugin/fast-crud/index.js （75-77行）
const { resetCrudOptions } = useCrud({
  crudExpose,
  crudOptions,
  context: {}
});
// 你可以调用此方法，重新初始化crud配置
// resetCrudOptions(options)
// 页面打开后获取列表数据
onMounted(async () => {
  await crudExpose.doRefresh();
  // const resp = await permission.getPermissionTree();
});
</script>
