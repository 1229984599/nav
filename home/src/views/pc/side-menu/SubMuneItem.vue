<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";

const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  iconSize: {
    type: [String, Number],
    default: 25,
  },
});
</script>

<template>
  <m-icon
    :size="iconSize"
    class="pr-1"
    :color="item?.color"
    :icon="item?.icon"
  />
  <span class="text-zinc-800 font-bold">
    {{ item.title }}
  </span>
</template>

<style lang="scss" scoped></style>
