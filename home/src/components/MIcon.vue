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
  color: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <div class="rounded-full flex items-center">
    <img
      v-if="isUrl(<string>props.icon)"
      class="icon-size"
      :width="size"
      height="auto"
      :src="icon"
      alt=""
    />
    <icon v-else :icon="icon" class="icon-size" :width="size" :height="size" />
  </div>
</template>

<style lang="scss" scoped>
.icon-size {
  @apply shadow-sm rounded-full;
  color: v-bind(color);
  object-fit: cover;
}
</style>
