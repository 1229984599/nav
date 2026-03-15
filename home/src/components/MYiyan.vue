<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getYiyan } from "@/api/spider";

const yiyan = ref("");
const props = defineProps({
  color: {
    type: String,
    default: "var(--nav-text-secondary)",
  },
});
async function refresh() {
  yiyan.value = await getYiyan();
}

onMounted(refresh);
</script>

<template>
  <span class="yiyan" @click="refresh">{{ yiyan }}</span>
</template>

<style lang="scss" scoped>
.yiyan {
  display: none;
  cursor: pointer;
  font-size: 0.87rem;
  line-height: 1.25rem;
  color: v-bind(color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  //pc端
  @media (min-width: 768px) {
    display: block;
  }
}
</style>
