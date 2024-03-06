<script lang="ts">
export default {
  name: "MTable",
};
</script>
<template>
  <fs-page>
    <fs-crud ref="crudRef" v-bind="crudBinding">
      <template v-for="name in $slots" :key="name" #[name]="data">
        <slot :name="name" v-bind="data" />
      </template>
    </fs-crud>
  </fs-page>
</template>

<script lang="ts" setup>
import { ref, onMounted, PropType } from "vue";
import { CrudOptions, useCrud, useExpose } from "@fast-crud/fast-crud";
import createCrudOptions from "./crud";
import { merge } from "lodash-es";
import type Crud from "@/api/crud";

const props = defineProps({
  model: {
    type: Object as PropType<Crud>,
    require: true,
  },
  // 你的crud配置
  crudOptions: {
    type: Object as PropType<CrudOptions>,
    required: true,
  },
});

// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置
const { crudOptions } = createCrudOptions(crudExpose, props.model);

const { resetCrudOptions } = useCrud({
  crudExpose,
  crudOptions: merge(crudOptions, props.crudOptions),
  context: {},
});
// 你可以调用此方法，重新初始化crud配置
// resetCrudOptions(options)
// 页面打开后获取列表数据
onMounted(async () => {
  await crudExpose.doRefresh();
  // const resp = await permission.getPermissionTree();
});
defineExpose({ crudExpose });
</script>
