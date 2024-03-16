<script setup lang="ts">
import ItemDesc from "./ItemDesc.vue";
import MIcon from "@/components/MIcon.vue";
import { PropType } from "vue";
import { MenuSchemaTree } from "@/api/menu/types";

defineProps({
  menu: {
    type: Object as PropType<MenuSchemaTree>,
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
    <slot name="title-action"></slot>
  </div>
  <div
    class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-x-4 md:gap-x-6 gap-y-4 mb-8 mt-3"
  >
    <item-desc :item="item" v-for="item in menu?.links">
      <template #local-action="{ item }">
        <slot name="local-action" :item="item"></slot>
      </template>
    </item-desc>
    <slot name="add-more"></slot>
  </div>
</template>

<style scoped></style>
