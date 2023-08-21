<script lang="ts">
export default {
  name: "MHeader",
};
</script>
<script setup lang="ts">
import MNavBar from "./navbar.vue";
</script>

<template>
  <div class="w-full h-full flex items-center border-b border-b-gray-200">
    <m-nav-bar />
  </div>
</template>

<style lang="scss" scoped></style>
