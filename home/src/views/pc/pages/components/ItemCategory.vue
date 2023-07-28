<script setup lang="ts">
import ItemDesc from "./ItemDesc.vue";
import MIcon from "@/components/MIcon.vue";
import { PropType } from "vue";
import { MenuType } from "@/api/menu";

defineProps({
  category: {
    type: Object as PropType<MenuType>,
  },
});
</script>

<template>
  <div :id="category?.title" class="flex gap-x-2 items-center">
    <m-icon v-if="category?.icon" class="text-red-900" :icon="category.icon" />
    <h2 class="text-xl font-bold">{{ category.title }}</h2>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-6 gap-x-6 gap-y-4 mb-8 mt-1">
    <item-desc :item="item" v-for="item in category?.navs" />
  </div>
</template>

<style scoped></style>
