<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { PropType } from "vue";
import { MenuSchemaTree } from "@/api/menu/types";

const props = defineProps({
  item: {
    type: Object as PropType<MenuSchemaTree>,
    default: () => ({}),
  },
  iconSize: {
    type: [String, Number],
    default: 25,
  },
});
</script>

<template>
  <div class="flex items-center">
    <m-icon
      :size="iconSize"
      class="pr-1"
      :color="item?.color"
      :icon="item?.icon"
    />
    <span class="text-zinc-800 font-bold">
      {{ item.title }}
    </span>
  </div>
</template>

<style lang="scss" scoped></style>
