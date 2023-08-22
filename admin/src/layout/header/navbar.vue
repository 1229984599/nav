<script lang="ts">
export default {
  name: "MNavBar",
};
</script>
<script setup lang="ts">
import { computed, ref } from "vue";
import MBreadcrumb from "./breadcrumb.vue";
import { useAppStore, useUserStore } from "@/store";
import MIcon from "@/components/icon.vue";
import MThemeSelect from "@/layout/header/theme-select/index.vue";
import { isMobile } from "@/utils/window";

const appStore = useAppStore();
const userStore = useUserStore();
const rotate = computed(() => {
  return appStore.isCollapse ? 0 : 2;
});
</script>

<template>
  <div class="flex justify-between items-center w-full">
    <!--    左侧-->
    <div class="flex items-center pl-2 space-x-3">
      <!--      菜单栏收缩按钮-->
      <m-icon
        @click="appStore.toggleCollapse"
        class="cursor-pointer"
        icon="ep:expand"
        size="25"
        :rotate="rotate"
      />
      <!--      面包屑导航-->
      <m-breadcrumb v-if="!isMobile" />
    </div>
    <!--    右侧-->
    <div class="flex items-center gap-x-2">
      <!--      主题切换-->
      <m-theme-select />
      <!--      个人中心-->
      <el-dropdown>
        <el-avatar
          class="cursor-pointer mr-4"
          src="https://img1.baidu.com/it/u=887091985,368385397&fm=253&fmt=auto&app=120&f=JPEG?w=502&h=500"
          size="default"
        />
        <template #dropdown>
          <el-dropdown-menu>
            <a href="/" class="hover:bg-zinc-600">主页 </a>
            <el-dropdown-item>修改密码</el-dropdown-item>
            <el-dropdown-item divided @click="userStore.logout"
              >退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<style lang="scss" scoped></style>
