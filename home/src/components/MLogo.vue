<script setup lang="ts">
import logo from "@/assets/logo.png";
</script>

<template>
  <div class="layout-logo-container px-5">
    <router-link
      key="collapse"
      class="flex decoration-none justify-center"
      to="/"
    >
      <img :src="logo" class="layout-logo" alt="logo" />
      <span class="logo-title">哈哈导航</span>
    </router-link>
  </div>
</template>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.layout-logo-container {
  display: flex;
  align-items: center;
  position: relative;
  z-index: 100;
  width: 100%;
  text-align: center;
  height: #{$navHeaderHeight};

  .layout-logo {
    width: 32px;
    height: 32px;
    vertical-align: middle;
    display: inline-block;
  }

  .logo-title {
    color: #1890ff;
    display: block;
    font-family: Avenir,
    Helvetica Neue,
    Arial,
    Helvetica,
    sans-serif;
    font-size: 20px;
    font-weight: 600;
    overflow: hidden;
    text-align: left;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .layout-logo-text {
    height: 100%;
    vertical-align: middle;
  }
}
</style>
