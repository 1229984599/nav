<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
</script>

<template>
  <el-dropdown>
    <span class="flex items-center">
      <m-icon
        icon="https://img1.baidu.com/it/u=1217061905,2277984247&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500"
      />
      <span>moxiaoying</span>
    </span>
    <template #dropdown>
      <el-dropdown-menu class="divide-2 divide-gray-300">
        <el-dropdown-item>个人中心</el-dropdown-item>
        <el-dropdown-item
          ><a href="/admin" target="_blank">后台管理</a></el-dropdown-item
        >
        <el-dropdown-item>退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style scoped></style>
