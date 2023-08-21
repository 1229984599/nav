<script lang="ts">
// 面包屑导航
export default {
  name: "MBreadcrumb",
};
</script>
<script setup lang="ts">
import { RouteLocationMatched, useRoute } from "vue-router";
import { ref, watch } from "vue";

const route = useRoute();
const breadcrumbList = ref<RouteLocationMatched[]>([]);
watch(
  route,
  () => {
    breadcrumbList.value = route.matched.filter((item) => item.meta?.title);
  },
  { immediate: true },
);
</script>

<template>
  <el-breadcrumb separator-icon="ArrowRight">
    <transition-group name="breadcrumb">
      <el-breadcrumb-item
        :to="breadcrumb.path"
        class="cursor-pointer"
        :key="breadcrumb.path"
        v-for="breadcrumb in breadcrumbList"
        >{{ breadcrumb.meta.title }}
      </el-breadcrumb-item>
    </transition-group>
  </el-breadcrumb>
</template>

<style lang="scss" scoped>
.breadcrumb-enter-active,
.breadcrumb-leave-active {
  transition: all 0.3s;
}

.breadcrumb-enter-from,
.breadcrumb-leave-active {
  opacity: 0;
  transform: translateX(20px);
}

.breadcrumb-leave-active {
  position: absolute;
}
</style>
