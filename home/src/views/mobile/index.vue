<script setup lang="ts">
import MMobileHeader from "./header/index.vue";
import MMobileMain from "./main/index.vue";
import MMobileFooter from "./footer/index.vue";
</script>

<template>
  <div class="mobile-container">
    <m-mobile-header />
    <m-mobile-main />
    <m-mobile-footer />
  </div>
</template>

<style scoped lang="scss">
.mobile-container {
  box-sizing: border-box;
  width: 100vw;
  height: 100vh;
  background-image: url("https://api.nnxv.cn/api/Bing.php");
  background-size: cover;
  background-position: center;
}
</style>
