<script lang="ts">
export default {
  name: "MSidebarMenu",
};
</script>
<script setup lang="ts">
// 处理路由数据
import { useRouter } from "vue-router";
import { filterRoutes, generateMenus } from "@/utils/route";
import MSidebarItem from "./sidebar-item.vue";
import { computed } from "vue";

const router = useRouter();
const allRoutes = router.getRoutes();
const routes = computed(() => {
  return generateMenus(filterRoutes(allRoutes));
});
// 只取meta含有title的路由
</script>

<template>
  <m-sidebar-item :key="route.path" :route="route" v-for="route in routes" />
</template>

<style lang="scss" scoped></style>
