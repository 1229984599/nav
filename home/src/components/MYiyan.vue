<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getYiyan } from "@/api/spider";

const yiyan = ref("");

async function refresh() {
  const { hitokoto, from } = await getYiyan();
  yiyan.value = `${hitokoto}\t——${from}`;
}

onMounted(refresh);
</script>

<template>
  <span
    @click="refresh"
    class="hidden md:flex cursor-pointer text-sm text-zinc-600 whitespace-nowrap overflow-x-clip w-2/3"
    >{{ yiyan }}</span
  >
</template>

<style lang="scss" scoped></style>
