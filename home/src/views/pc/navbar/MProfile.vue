<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
</script>

<template>
  <el-dropdown>
    <span class="flex items-center">
      <m-icon icon="octicon:person-16" />
      <span>moxiaoying</span>
    </span>
    <template #dropdown>
      <el-dropdown-menu class="divide-2 divide-gray-300">
        <el-dropdown-item>个人中心</el-dropdown-item>
        <el-dropdown-item>退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style scoped></style>
