<script setup lang="ts">
import { useSiteStore } from "@/store/site";
import MIcon from "@/components/MIcon.vue";
defineProps({
  fontSize: {
    type: String,
    default: "20px",
  },
});
const siteStore = useSiteStore();
</script>

<template>
  <div class="layout-logo-container px-5">
    <a
      key="collapse"
      class="flex decoration-none items-center justify-center"
      href="/"
    >
      <m-icon
        :icon="siteStore.siteInfo?.icon"
        :size="40"
        :color="siteStore.siteInfo?.color"
      />
      <span class="logo-title" :style="{ color: siteStore.siteInfo?.color }">{{
        siteStore.siteInfo?.title
      }}</span>
    </a>
  </div>
</template>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.layout-logo-container {
  display: flex;
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
    padding-left: 2px;
    font-size: v-bind(fontSize);
    font-weight: 700;
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
