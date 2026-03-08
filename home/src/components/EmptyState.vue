<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";

defineOptions({ name: "EmptyState" });

withDefaults(
  defineProps<{
    icon?: string;
    text?: string;
    actionText?: string;
    size?: number;
  }>(),
  {
    icon: "mdi:inbox-outline",
    text: "暂无数据",
    size: 48,
  },
);

defineEmits<{
  (e: "action"): void;
}>();
</script>

<template>
  <div class="empty-state">
    <m-icon :icon="icon" :size="size" color="#dcdfe6" />
    <p>{{ text }}</p>
    <el-button v-if="actionText" type="primary" size="small" @click="$emit('action')">
      {{ actionText }}
    </el-button>
  </div>
</template>

<style lang="scss" scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 36px 0 28px;
  gap: 10px;
  color: var(--nav-text-secondary);
  font-size: 13px;
}
</style>
