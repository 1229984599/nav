<script lang="ts">
export default {
  name: "MMask",
};
</script>
<script setup lang="ts">
defineProps({
  isMask: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <div v-show="isMask" class="mask"></div>
</template>

<style lang="scss" scoped>
.mask {
  position: fixed;
  right: 0;
  top: 0;
  z-index: 20;
  cursor: pointer;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
}
</style>
