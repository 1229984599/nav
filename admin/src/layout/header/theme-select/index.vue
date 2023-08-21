<script lang="ts">
export default {
  name: "MThemeSelect",
};
</script>
<script setup lang="ts">
import MIcon from "@/components/icon.vue";
import MSelectColor from "./SelectColor.vue";
import { ref } from "vue";

const selectColorVisible = ref(false);
const handleSetTheme = (command) => {
  selectColorVisible.value = true;
};
</script>
<template>
  <!-- 主题图标
  v-bind：https://v3.cn.vuejs.org/api/instance-properties.html#attrs -->
  <el-dropdown
    v-bind="$attrs"
    trigger="click"
    class="theme"
    @command="handleSetTheme"
  >
    <div>
      <el-tooltip content="切换主题">
        <m-icon size="26" icon="mdi:theme-light-dark" />
      </el-tooltip>
    </div>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="color"> 切换主题</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
  <!-- 展示弹出层 -->
  <div>
    <m-select-color v-model="selectColorVisible" />
  </div>
</template>

<style lang="scss" scoped></style>
