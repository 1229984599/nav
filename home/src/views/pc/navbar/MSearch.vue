<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { ref } from "vue";

const searchQuery = ref("");

async function querySearchAsync() {}

function handleSubmit() {}
</script>

<template>
  <el-autocomplete
    hide-loading
    highlight-first-item
    clearable
    fit-input-width
    class="w-full h-full"
    v-model="searchQuery"
    :fetch-suggestions="querySearchAsync"
    placeholder="电视剧 / 电影 / 动漫 / 综艺 ..."
  >
    <template #default="{ item }">
      <div class="flex justify-between">
        <span class="px-2">{{ item.title }}</span>
        <span>{{ item.cat_name }}</span>
      </div>
    </template>
    <template #prefix>
      <m-icon
        class="cursor-pointer text-gray-400"
        icon="mdi:search"
        @click="handleSubmit"
      />
    </template>
  </el-autocomplete>
</template>

<style lang="scss" scoped>
//:deep(.el-input__clear) {
//  @apply absolute right-12;
//}

:deep(.el-autocomplete > .el-input > .el-input__wrapper) {
  border-radius: 9999px;
}
</style>
