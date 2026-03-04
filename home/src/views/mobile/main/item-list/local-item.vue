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
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.12));
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  box-shadow:
    0 10px 24px rgba(5, 12, 38, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
  padding: 16px 12px;
  backdrop-filter: blur(22px) saturate(1.12);
  -webkit-backdrop-filter: blur(22px) saturate(1.12);

  .bookmark-header h2,
  .bookmark-header .header-count {
    color: rgba(255, 255, 255, 0.96);
    text-shadow: 0 2px 8px rgba(8, 13, 23, 0.2);
  }

  .header-count {
    background: rgba(255, 255, 255, 0.3) !important;
  }

  .group-tab {
    background-color: rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.92);
    border-color: rgba(255, 255, 255, 0.24);

    .tab-badge {
      background: rgba(255, 255, 255, 0.24);
      color: #fff;
    }

    &.active {
      background: linear-gradient(135deg, rgba(69, 140, 255, 0.92), rgba(134, 196, 255, 0.82));
      color: #fff;
      border-color: transparent;
      box-shadow: 0 7px 15px rgba(34, 112, 255, 0.28);

      .tab-badge {
        background: rgba(255, 255, 255, 0.28);
        color: #fff;
      }
    }

    &.tab-add {
      border-color: rgba(255, 255, 255, 0.34);
      color: rgba(255, 255, 255, 0.86);
    }
  }

  .bookmark-empty {
    color: rgba(255, 255, 255, 0.76);
  }

  // Grid 视图
  .card-wrap {
    background-color: rgba(255, 255, 255, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.22);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.28);
  }

  .bk-card {
    color: #fff;
    .card-desc {
      color: rgba(255, 255, 255, 0.74);
    }
    .card-visits {
      background: rgba(255, 255, 255, 0.22);
      color: rgba(255, 255, 255, 0.9);
    }
  }

  .card-bar {
    border-top-color: rgba(255, 255, 255, 0.16);
    color: rgba(255, 255, 255, 0.74);

    .bar-btn {
      color: rgba(255, 255, 255, 0.76);
      &:hover {
        background: rgba(255, 255, 255, 0.22);
        color: #fff;
      }
    }
  }

  // Compact 视图
  .compact-item {
    color: #fff;

    .compact-icon {
      background: rgba(255, 255, 255, 0.2);
    }

    .compact-group {
      color: rgba(255, 255, 255, 0.64);
    }
  }

  // List 视图
  .list-row {
    color: #fff;
    &:hover {
      background-color: rgba(255, 255, 255, 0.12);
    }

    .list-url {
      color: rgba(255, 255, 255, 0.64);
    }

    .list-group-tag {
      background: rgba(255, 255, 255, 0.2);
      color: rgba(255, 255, 255, 0.8);
    }

    .list-visits {
      color: rgba(255, 255, 255, 0.64);
    }

    .list-action {
      color: rgba(255, 255, 255, 0.74);
      &:hover {
        background: rgba(255, 255, 255, 0.22);
        color: #fff;
      }
    }
  }
}
</style>
