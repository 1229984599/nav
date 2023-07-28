<script setup lang="ts">
import { computed } from "vue";
import { Icon } from "@iconify/vue";

defineOptions({
  name: "MIcon",
});
const props = defineProps({
  icon: {
    type: String,
    default: "",
  },
  size: {
    typer: [String, Number],
    default: 32,
  },
});
const isUrl = computed(() => {
  // 判断props.icon是否为url
  const regex = new RegExp(`^(https?:)?//.+`);
  return regex.test(props.icon);
});
</script>

<template>
  <div class="rounded-full flex items-center">
    <img v-if="isUrl" class="icon-size" :src="icon" alt="" />
    <icon v-else :icon="icon" :width="size" :height="size" />
  </div>
</template>

<style lang="scss" scoped></style>
