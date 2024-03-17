<script setup lang="ts">
import { useMenuStore } from "@/store/menu";
import MIcon from "@/components/MIcon.vue";

import MLocalMenu from "@/components/local-menu/index.vue";

defineOptions({
  name: "MMobileLocalItem",
});
const menuStore = useMenuStore();
</script>

<template>
  <m-local-menu
    class-name="w-full mx-auto md:w-[50%] min-h-[200px] max-h-[300px] md:max-h-[350px] overflow-hidden grid grid-cols-4 md:grid-cols-7 gap-y-4 items-center bg-black/20 py-2 md:py-4 rounded-md  backdrop-blur-[2px]"
  >
    <template #menu-title><div></div></template>
    <template #item-desc="{ item }">
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
    </template>
    <template #add-more>
      <m-icon
        class="add-more"
        icon="ci:file-add"
        size="50"
        :color="menuStore.localMenu.color"
      />
    </template>
  </m-local-menu>
</template>

<style scoped lang="scss">
.item-container {
  width: 50%;
  margin: auto;
  @media screen and (max-width: 768px) {
    width: 100%;
  }

  & > .item {
    width: 100px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    //align-items: stretch;
    row-gap: 10px;
    text-decoration: none;
    color: inherit;
    cursor: pointer;
    transition: all 0.3s ease;
    @media screen and (max-width: 768px) {
      width: 60px;
    }

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
        font-size: 12px;
        padding: 2px 10px;
      }
    }
  }
}

.add-more {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 999px;
  background: rgba(231, 226, 226, 0.4);
  cursor: pointer;
  width: 100px;
  height: 100px;
  margin: auto;
  @media screen and (max-width: 768px) {
    width: 60px;
    height: 60px;
  }
}
</style>
