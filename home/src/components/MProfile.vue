<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";

const props = defineProps({
  color: {
    type: String,
    default: "",
  },
});
const userStore = useUserStore();
</script>

<template>
  <el-dropdown v-if="userStore.token?.access_token">
    <span class="flex items-center gap-x-1">
      <m-icon
        :size="26"
        icon="https://img1.baidu.com/it/u=1217061905,2277984247&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500"
      />
      <span
        :style="{
          color: props.color,
        }"
        >{{ userStore.userInfo?.nickname }}</span
      >
    </span>
    <template #dropdown>
      <el-dropdown-menu class="divide-2 divide-gray-300">
        <el-dropdown-item
          ><a href="/admin" target="_blank">后台管理</a></el-dropdown-item
        >
        <el-dropdown-item divided @click="userStore.logout"
          >退出登录
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
  <router-link
    :to="{ name: 'Login' }"
    class="font-bold mr-2"
    :style="{
      color: props.color,
    }"
    v-else
  >
    登录
  </router-link>
</template>

<style scoped></style>
