<script setup lang="ts">
import { useSiteStore } from "@/store/site";
import MIcon from "@/components/MIcon.vue";

const siteStore = useSiteStore();
</script>

<template>
  <div class="layout-logo-container px-5">
    <router-link
      key="collapse"
      class="flex decoration-none items-center justify-center"
      to="/"
    >
      <m-icon
        :icon="siteStore.siteInfo?.icon"
        :size="40"
        :color="siteStore.siteInfo?.color"
      />
      <span class="logo-title" :style="{ color: siteStore.siteInfo?.color }">{{
        siteStore.siteInfo?.title
      }}</span>
    </router-link>
  </div>
</template>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.layout-logo-container {
  display: flex;
  background-color: #fff;
  align-items: center;
  position: relative;
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
    display: block;
    font-family:
      Avenir,
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
