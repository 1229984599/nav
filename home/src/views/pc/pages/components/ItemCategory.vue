<script setup lang="ts">
import ItemDesc from "./ItemDesc.vue";
import MIcon from "@/components/MIcon.vue";
import { PropType } from "vue";

defineProps({
  menu: {
    type: Object,
  },
});
</script>

<template>
  <div :id="menu?.title" class="flex gap-x-2 items-center">
    <m-icon
      v-if="menu?.icon"
      :style="{ color: menu?.color }"
      :icon="menu.icon"
    />
    <h2 class="text-xl font-bold">{{ menu?.title }}</h2>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-5 gap-x-6 gap-y-4 mb-8 mt-3">
    <item-desc :item="item" v-for="item in menu?.links" />
  </div>
</template>

<style scoped></style>
