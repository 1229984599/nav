<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { useAppStore } from "@/store/app";
import { onMounted, ref } from "vue";
import { getYiyan } from "@/api/yiyan";
import MProfile from "@/views/pc/navbar/MProfile.vue";
import MSearch from "@/views/pc/navbar/MSearch.vue";

const appStore = useAppStore();
const yiyan = ref("");

async function refresh() {
  const { hitokoto, from } = await getYiyan();
  yiyan.value = `${hitokoto}\t——${from}`;
}

onMounted(refresh);
</script>

<template>
  <div class="flex items-center justify-between h-full">
    <m-icon
      @click="appStore.toggleSlide()"
      class="cursor-pointer px-2"
      icon="ph:list-fill"
    />
    <div class="w-full flex items-center justify-between">
      <div class="w-1/4">
        <m-search />
      </div>
      <span></span>
      <span
        @click="refresh"
        class="hidden md:flex cursor-pointer text-sm text-zinc-600 whitespace-nowrap text-ellipsis w-2/3 justify-center"
        >{{ yiyan }}</span
      >
      <m-profile class="mr-1" />
    </div>
  </div>
</template>

<style scoped></style>
