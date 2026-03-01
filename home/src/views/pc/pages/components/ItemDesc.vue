<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { PropType } from "vue";
import { LinkSchemaList } from "@/api/links/types";

const props = defineProps({
  item: {
    type: Object as PropType<LinkSchemaList>,
    required: true,
  },
  showDragHandle: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits<{
  (e: "contextmenu", event: MouseEvent, item: LinkSchemaList): void;
}>();

function handleContextMenu(event: MouseEvent) {
  emit("contextmenu", event, props.item);
}
</script>

<template>
  <div class="relative w-full" v-if="item?.status" @contextmenu="handleContextMenu">
    <div v-if="showDragHandle" class="link-drag-handle">
      <m-icon icon="mdi:drag" :size="16" color="#9ca3af" />
    </div>
    <el-tooltip :disabled="!item?.desc" :hide-after="200" :enterable="false">
      <a
        :href="item?.href"
        :target="item?.is_self ? '_self' : '_blank'"
        class="box space-x-2"
      >
        <div class="left-icon">
          <m-icon
            :color="item?.color"
            :icon="item?.icon"
            :size="45"
            class="rounded-full"
          />
        </div>

        <div class="right-content">
          <span class="title">{{ item.title }}</span>
          <p class="desc">
            {{ item?.desc || "暂无描述信息" }}
          </p>
        </div>
      </a>
      <template #content>
        <div style="max-width: 300px">{{ item.desc }}</div>
      </template>
    </el-tooltip>
  </div>
</template>

<style lang="scss" scoped>
.link-drag-handle {
  position: absolute;
  top: 2px;
  right: 2px;
  z-index: 10;
  cursor: move;
  opacity: 0;
  transition: opacity 0.2s ease;
  background: var(--nav-card-bg);
  border-radius: 4px;
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover :deep(svg) {
    color: #4b5563 !important;
  }
}

.relative:hover .link-drag-handle {
  opacity: 1;
}

.box {
  display: inline-flex;
  width: 100%;
  height: 100%;
  align-items: center;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  background-color: var(--nav-card-bg);
  padding: 8px;
  border-radius: 8px;
  transition:
    box-shadow 0.3s,
    transform 0.3s,
    color 0.3s;

  &:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加底部阴影 */
    transform: translateY(-2px); /* 向上移动一点的动画效果 */
    color: var(--el-color-primary);
  }

  & > .left-icon {
    flex-shrink: 0;
    //flex-basis: 13%;
  }

  & > .right-content {
    flex-basis: 87%;
    overflow: hidden;

    & > .title {
      font-size: 1rem;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      display: inline-block;
      //移动样式
      @media screen and (max-width: 768px) {
        font-size: 0.88rem;
      }
    }

    & > .desc {
      min-height: 36px;
      text-overflow: ellipsis;
      word-break: break-all;
      overflow: hidden;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      color: var(--nav-text-secondary);
      font-size: 0.75rem;
    }
  }

  //pc样式
  @media screen and (min-width: 769px) {
    padding: 16px;
    & > .right-content {
      padding-left: 4px;
    }
  }
}
</style>
