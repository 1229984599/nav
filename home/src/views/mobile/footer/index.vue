<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { useAppStore } from "@/store/app";

defineOptions({ name: "MMobileFooter" });
const appStore = useAppStore();
</script>

<template>
  <div class="footer-container">
    <el-tooltip content="返回主页" placement="left">
      <router-link :to="{ name: 'List' }">
        <m-icon class="footer-icon" size="30" icon="el:iphone-home" />
      </router-link>
    </el-tooltip>
    <el-tooltip content="随机背景图片" placement="left">
      <m-icon
        @click.stop="appStore.getRandomBg"
        class="footer-icon"
        size="30"
        icon="majesticons:image-circle"
      />
    </el-tooltip>
  </div>
</template>

<style scoped lang="scss">
.footer-container {
  position: absolute;
  right: 10px;
  bottom: 24px;
  display: flex;
  flex-direction: column;
  row-gap: 8px;
  cursor: pointer;
  .footer-icon {
    color: #2e97ff;
    transition: color 0.3s ease;
    &:hover {
      color: #934ad9;
    }
  }
}
</style>
