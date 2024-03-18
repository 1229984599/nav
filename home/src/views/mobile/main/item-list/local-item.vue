<script setup lang="ts">
import { useMenuStore } from "@/store/menu";
import MIcon from "@/components/MIcon.vue";

import { VueDraggable } from "vue-draggable-plus";
import MLocalMenu from "@/components/local-menu/index.vue";
import { ref } from "vue";

defineOptions({
  name: "MMobileLocalItem",
});
const menuStore = useMenuStore();
const linkRef = ref();
</script>

<template>
  <m-local-menu ref="linkRef">
    <template #menu-title>
      <div></div>
    </template>
    <template #item-list>
      <VueDraggable
        class="item-list grid grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 2xl:grid-cols-8 gap-x-4 md:gap-x-6 gap-y-6"
        v-model="menuStore.localMenu.links"
        filter=".add-more"
      >
        <div
          class="item-container"
          :key="item.href"
          v-for="item in menuStore.localMenu.links"
        >
          <a
            class="item"
            :href="item.href"
            :target="item?.is_self ? '_self' : '_blank'"
          >
            <div class="item-icon">
              <m-icon :icon="item.icon" size="50" :color="item.color" />
            </div>
            <span class="item-title">{{ item.title }}</span>
          </a>
          <div class="local-action">
            <m-icon
              class="edit-action"
              @click.stop="
                () => {
                  linkRef.action.handleEdit(item);
                }
              "
              size="20"
              color="#409eff"
              icon="mdi:circle-edit-outline"
            />
            <el-popconfirm
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="
                () => {
                  linkRef.action.handleDelete(item);
                }
              "
              title="确定要删除吗？"
            >
              <template #reference>
                <m-icon
                  class="delete-action"
                  size="24"
                  color="#f56c6c"
                  icon="typcn:delete"
                />
              </template>
            </el-popconfirm>
          </div>
        </div>
        <el-tooltip content="添加本地书签">
          <div
            @click.stop="
              () => {
                linkRef.action.handleAddLink();
              }
            "
          >
            <slot name="add-more">
              <m-icon
                class="add-more w-full"
                icon="ci:file-add"
                size="50"
                :color="menuStore.localMenu.color"
              />
            </slot>
          </div>
        </el-tooltip>
      </VueDraggable>
    </template>
  </m-local-menu>
</template>

<style scoped lang="scss">
.item-list {
  width: 100%;
  margin: auto;
  align-items: center;
  background-color: rgb(0 0 0 / 0.2);
  border-radius: 0.375rem /* 6px */;
  padding: 26px 10px;
  min-height: 200px;
  max-height: 380px;
  overflow-x: hidden;
  overflow-y: auto;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  @media screen and (max-width: 768px) {
    width: 100%;
    max-height: 360px;
  }

  .item-container {
    position: relative;

    & > .item {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      row-gap: 10px;
      margin: auto;
      text-decoration: none;
      color: inherit;
      cursor: pointer;
      transition: all 0.3s ease;
      &:hover {
        transform: scale(1.1);
      }

      & > .item-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 50px;
        //background-color: white;
        //border-radius: 999px;
      }

      & > .item-title {
        display: block;
        padding: 4px 12px;
        text-align: center;
        max-width: 100%;
        width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size: 14px;
        background-color: rgba(231, 228, 228, 0.5);
        color: #fff;
        border-radius: 20px;
        @media screen and (max-width: 768px) {
          font-size: 10px;
          padding: 4px 10px;
        }
      }
    }

    &:hover > .local-action {
      visibility: visible;
      opacity: 1;
    }

    & > .local-action {
      visibility: hidden;
      opacity: 0;
      transition: all 0.3s ease;
      cursor: pointer;

      .edit-action {
        position: absolute;
        left: -8px;
        top: -10px;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 999px;
        transition: all 0.3s ease;
        &:hover {
          transform: scale(1.3);
          box-shadow: rebeccapurple 0 0 2px 0;
        }
        @media screen and (min-width: 769px) {
          left: 2px;
          top: -10px;
        }
      }

      .delete-action {
        position: absolute;
        right: -8px;
        top: -10px;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 999px;
        transition: all 0.3s ease;

        &:hover {
          transform: scale(1.2);
          box-shadow: rebeccapurple 0 0 2px 0;
        }
        @media screen and (min-width: 769px) {
          right: 2px;
          top: -10px;
        }
      }
    }
  }

  & .add-more {
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 999px;
    background: rgba(231, 226, 226, 0.4);
    cursor: pointer;
    width: 90px;
    height: 90px;
    margin: auto;
    transition: all 0.3s ease;
    @media screen and (max-width: 768px) {
      width: 60px;
      height: 60px;
    }

    &:hover {
      transform: scale(1.1);
    }
  }
}
</style>
