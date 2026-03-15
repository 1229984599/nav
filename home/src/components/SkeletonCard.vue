<script setup lang="ts">
defineOptions({ name: "SkeletonCard" });

withDefaults(
  defineProps<{
    count?: number;
    type?: "card" | "menu" | "weather";
  }>(),
  {
    count: 8,
    type: "card",
  },
);
</script>

<template>
  <!-- 卡片骨架 -->
  <template v-if="type === 'card'">
    <div
      v-for="i in count"
      :key="i"
      class="sk-card skeleton-pulse"
    >
      <div class="sk-card-icon" />
      <div class="sk-card-body">
        <div class="sk-line sk-line-title" />
        <div class="sk-line sk-line-desc" />
        <div class="sk-line sk-line-desc sk-line-short" />
      </div>
    </div>
  </template>

  <!-- 菜单骨架 -->
  <template v-else-if="type === 'menu'">
    <div
      v-for="i in count"
      :key="i"
      class="sk-menu skeleton-pulse"
    >
      <div class="sk-menu-icon" />
      <div class="sk-line sk-menu-text" />
    </div>
  </template>

  <!-- 热榜条目骨架 -->
  <template v-else-if="type === 'weather'">
    <div
      v-for="i in count"
      :key="i"
      class="sk-hot-row skeleton-pulse"
    >
      <div class="sk-hot-index" />
      <div class="sk-line sk-hot-title" />
      <div class="sk-line sk-hot-num" />
    </div>
  </template>
</template>

<style lang="scss" scoped>
$sk-bg: var(--el-fill-color, #e9ecef);
$sk-radius: 4px;

/* 卡片骨架 */
.sk-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background-color: var(--nav-card-bg);
  border-radius: 8px;
}

.sk-card-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: $sk-bg;
  flex-shrink: 0;
}

.sk-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sk-line {
  height: 12px;
  background: $sk-bg;
  border-radius: $sk-radius;
}

.sk-line-title {
  width: 60%;
  height: 14px;
}

.sk-line-desc {
  width: 90%;
}

.sk-line-short {
  width: 50%;
}

/* 菜单骨架 */
.sk-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
}

.sk-menu-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: $sk-bg;
  flex-shrink: 0;
}

.sk-menu-text {
  width: 70%;
  height: 14px;
}

/* 热榜骨架 */
.sk-hot-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
}

.sk-hot-index {
  width: 22px;
  height: 18px;
  border-radius: 3px;
  background: $sk-bg;
  flex-shrink: 0;
}

.sk-hot-title {
  flex: 1;
  height: 14px;
}

.sk-hot-num {
  width: 36px;
  height: 12px;
}
</style>
