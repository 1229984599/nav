<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { isUrl } from "@/utils/window";

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
</script>

<template>
  <div class="rounded-full flex items-center">
    <img
      v-if="isUrl(<string>props.icon)"
      class="icon-size"
      :src="icon"
      alt=""
    />
    <icon v-else :icon="icon" :width="size" :height="size" />
  </div>
</template>

<style lang="scss" scoped>
img {
  @apply shadow-sm border border-gray-200;
}
</style>
