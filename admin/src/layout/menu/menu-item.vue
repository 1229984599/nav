<script lang="ts">
export default {
  name: "MMenuItem",
};
</script>
<script setup lang="ts">
import { defineProps } from "vue";
import MIcon from "@/components/icon.vue";

defineProps({
  title: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
  },
});
</script>

<template>
  <m-icon class="mr-1" :size="18" :icon="icon" />
  <span class="font-bold">{{ title }}</span>
</template>

<style lang="scss" scoped></style>
