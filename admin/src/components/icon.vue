<script setup lang="ts">
import { computed } from "vue";
import { Icon } from "@iconify/vue";
import { isUrl } from "@/utils/window";

defineOptions({
  name: "MIcon",
});

const props = withDefaults(
  defineProps<{
    icon?: string;
    size?: string | number;
    color?: string;
  }>(),
  {
    icon: "",
    size: 16,
    color: "",
  },
);

const isImageUrl = computed(() => isUrl(props.icon));
const hasIcon = computed(() => Boolean(props.icon));
</script>

<template>
  <img
    v-if="hasIcon && isImageUrl"
    v-bind="$attrs"
    class="icon-size"
    :width="props.size"
    height="auto"
    :src="props.icon"
    alt=""
  />
  <Icon
    v-else-if="hasIcon"
    v-bind="$attrs"
    :icon="props.icon"
    class="icon-size"
    :width="props.size"
    :height="props.size"
  />
  <span v-else class="icon-size" :style="{ width: `${props.size}px`, display: 'inline-block' }"></span>
</template>

<style lang="scss" scoped>
.icon-size {
  color: v-bind("props.color");
  object-fit: fill;
}
</style>

