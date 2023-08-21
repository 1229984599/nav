<script lang="ts">
export default {
  name: "MSidebarItem",
};
</script>
<script setup lang="ts">
import { PropType } from "vue";
import { RouteRecordRaw } from "vue-router";
import MMenuItem from "./menu-item.vue";

const props = defineProps({
  route: {
    type: Object as PropType<RouteRecordRaw>,
    required: true,
  },
});
</script>

<template>
  <el-sub-menu v-if="route?.children?.length" :index="route.path">
    <template #title><m-menu-item v-bind="route.meta" /></template>
    <el-menu-item v-for="item in route.children" :index="item.path">
      <m-menu-item v-bind="item.meta" />
    </el-menu-item>
  </el-sub-menu>
  <el-menu-item v-else :index="route.path">
    <m-menu-item v-bind="route.meta" />
  </el-menu-item>
</template>

<style lang="scss" scoped></style>
