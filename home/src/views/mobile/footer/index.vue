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
        <m-icon class="footer-icon" size="28" icon="el:iphone-home" />
      </router-link>
    </el-tooltip>
    <el-tooltip content="随机背景图片" placement="left">
      <m-icon
        @click.stop="appStore.getRandomBg"
        class="footer-icon"
        size="28"
        icon="majesticons:image-circle"
      />
    </el-tooltip>
  </div>
</template>

<style scoped lang="scss">
.footer-container {
  position: fixed;
  left: 50%;
  bottom: 18px;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.36), rgba(255, 255, 255, 0.16));
  backdrop-filter: blur(18px) saturate(1.14);
  -webkit-backdrop-filter: blur(18px) saturate(1.14);
  box-shadow:
    0 10px 24px rgba(2, 9, 28, 0.24),
    inset 0 1px 0 rgba(255, 255, 255, 0.52);
  z-index: 6;

  a {
    display: inline-flex;
    text-decoration: none;
  }

  .footer-icon {
    color: rgba(255, 255, 255, 0.95);
    cursor: pointer;
    padding: 8px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.2);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.36);
    transition: transform 0.25s ease, background-color 0.25s ease, color 0.25s ease;

    &:hover {
      transform: translateY(-6px) scale(1.08);
      background: rgba(91, 161, 255, 0.28);
      color: #ffffff;
    }
  }
}

@media screen and (max-width: 768px) {
  .footer-container {
    bottom: 14px;
    gap: 10px;
    padding: 8px 10px;

    .footer-icon {
      padding: 6px;
      border-radius: 10px;
    }
  }
}
</style>
