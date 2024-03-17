<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";

defineOptions({ name: "MMobileFooter" });
</script>

<template>
  <div class="absolute right-2 bottom-6">
    <el-tooltip content="返回主页" placement="left">
      <router-link :to="{ name: 'List' }">
        <m-icon
          class="hover:text-red-600 bg-white rounded-full"
          size="30"
          icon="ion:home-sharp"
        />
      </router-link>
    </el-tooltip>
  </div>
</template>

<style scoped lang="scss"></style>
