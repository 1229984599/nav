<script lang="ts">
export default {
  name: "MSelectTree",
};
</script>
<script setup lang="ts">
import { useVModel } from "@vueuse/core";
import { onMounted, ref } from "vue";
import menuModel from "@/api/menu";
import { useMenuStore } from "@/store";

const props = defineProps({
  modelValue: {
    required: true,
  },
});
const Tree = useVModel(props, "modelValue");
const dataList = ref([]);
const menuStore = useMenuStore();
async function getDataList() {
  const items = await menuModel.getMenuTree();
  dataList.value = items;
  return items;
}

onMounted(menuStore.getMenuTree);
</script>

<template>
  <el-tree-select
    v-bind="$attrs"
    v-model="Tree"
    :data="menuStore.menuTree"
    :render-after-expand="false"
    show-checkbox
    check-strictly
    check-on-click-node
    default-expanded-keys
    highlight-current
    filterable
    clearable
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
        <span>{{ data.title }}</span>
      </div>
    </template>
  </el-tree-select>
</template>

<style lang="scss" scoped></style>
