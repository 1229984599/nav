<script setup lang="ts">
import { onMounted } from "vue";
import { useUserStore } from "@/store/user";

const userStore = useUserStore();

onMounted(() => {
  userStore.verifyAdminSession();
});
</script>

<template>
  <router-view></router-view>
</template>

<style scoped></style>
