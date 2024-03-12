<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { PropType, ref } from "vue";
import { LinkSchemaList } from "@/api/links/types";
import { useElementSize } from "@vueuse/core";

defineProps({
  item: {
    type: Object as PropType<LinkSchemaList>,
    required: true,
  },
});
const itemRef = ref<HTMLElement>();
const { width } = useElementSize(itemRef);
</script>

<template>
  <div class="relative" v-if="item?.status">
    <el-tooltip :disabled="!item?.desc" :hide-after="200" :enterable="false">
      <a
        ref="itemRef"
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
        <div :style="{ maxWidth: width + 'px' }">{{ item.desc }}</div>
      </template>
    </el-tooltip>
    <!--    本地书签操作按钮 编辑，删除-->
    <slot :item="item" name="local-action"></slot>
  </div>
</template>

<style lang="scss" scoped>
.box {
  display: inline-flex;
  width: 100%;
  height: 100%;
  align-items: center;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  background-color: white;
  padding: 8px;
  border-radius: 8px;
  transition:
    box-shadow 0.3s,
    transform 0.3s,
    color 0.3s;

  &:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加底部阴影 */
    transform: translateY(-2px); /* 向上移动一点的动画效果 */
    color: #cc2b2b;
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
      --tw-text-opacity: 1;
      color: rgb(156 163 175 / var(--tw-text-opacity));
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
