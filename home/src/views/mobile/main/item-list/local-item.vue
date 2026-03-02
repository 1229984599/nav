<script setup lang="ts">
import BookmarkSection from "@/components/local-menu/BookmarkSection.vue";

defineOptions({
  name: "MMobileLocalItem",
});
</script>

<template>
  <bookmark-section mobile />
</template>

<style scoped lang="scss">
:deep(.bookmark-section) {
  background-color: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  padding: 16px 12px;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);

  .bookmark-header h2,
  .bookmark-header .header-count {
    color: #fff;
  }

  .header-count {
    background: rgba(255, 255, 255, 0.25) !important;
  }

  .group-tab {
    background-color: rgba(231, 228, 228, 0.3);
    color: #fff;
    border-color: transparent;

    .tab-badge {
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
    }

    &.active {
      background-color: var(--el-color-primary);
      color: #fff;
      border-color: transparent;

      .tab-badge {
        background: rgba(255, 255, 255, 0.3);
        color: #fff;
      }
    }

    &.tab-add {
      border-color: rgba(255, 255, 255, 0.4);
      color: rgba(255, 255, 255, 0.8);
    }
  }

  .bookmark-empty {
    color: rgba(255, 255, 255, 0.7);
  }

  // Grid 视图
  .card-wrap {
    background-color: rgba(255, 255, 255, 0.15);
  }

  .bk-card {
    color: #fff;
    .card-desc {
      color: rgba(255, 255, 255, 0.7);
    }
    .card-visits {
      background: rgba(255, 255, 255, 0.2);
      color: rgba(255, 255, 255, 0.9);
    }
  }

  .card-bar {
    border-top-color: rgba(255, 255, 255, 0.15);
    color: rgba(255, 255, 255, 0.7);

    .bar-btn {
      color: rgba(255, 255, 255, 0.7);
      &:hover {
        background: rgba(255, 255, 255, 0.15);
        color: #fff;
      }
    }
  }

  // Compact 视图
  .compact-item {
    color: #fff;

    .compact-icon {
      background: rgba(255, 255, 255, 0.15);
    }

    .compact-group {
      color: rgba(255, 255, 255, 0.6);
    }
  }

  // List 视图
  .list-row {
    color: #fff;
    &:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }

    .list-url {
      color: rgba(255, 255, 255, 0.6);
    }

    .list-group-tag {
      background: rgba(255, 255, 255, 0.15);
      color: rgba(255, 255, 255, 0.8);
    }

    .list-visits {
      color: rgba(255, 255, 255, 0.6);
    }

    .list-action {
      color: rgba(255, 255, 255, 0.7);
      &:hover {
        background: rgba(255, 255, 255, 0.15);
        color: #fff;
      }
    }
  }
}
</style>
