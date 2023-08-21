<script lang="ts">
export default {
  name: "MIcon",
};
</script>
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
    default: 16,
  },
  color: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <img
    v-if="isUrl(<string>props.icon)"
    v-bind="$attrs"
    class="icon-size"
    :width="size"
    height="auto"
    :src="icon"
    alt=""
  />
  <icon
    v-else
    v-bind="$attrs"
    :icon="icon"
    class="icon-size"
    :width="size"
    :height="size"
  />
</template>

<style lang="scss" scoped>
.icon-size {
  color: v-bind(color);
  object-fit: fill;
}
</style>
