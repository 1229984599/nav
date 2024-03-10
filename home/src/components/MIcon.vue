<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { isUrl } from "@/utils/window";

defineOptions({
  name: "MIcon",
});
const props = defineProps({
  icon: {
    type: [String],
    default: "",
  },
  size: {
    typer: [String, Number],
    default: 32,
  },
});
</script>

<template>
  <div class="flex items-center">
    <img
      v-if="isUrl(<string>props.icon)"
      :width="size"
      height="auto"
      :src="icon"
      alt=""
    />
    <icon v-else :icon="icon" v-bind="$attrs" :width="size" :height="size" />
  </div>
</template>

<style lang="scss" scoped>
img {
  object-fit: fill;
  border-radius: 999px;
}
</style>
