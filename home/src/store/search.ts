import { defineStore } from "pinia";
// @ts-ignore
import {
  catItemType,
  catSearchList,
  catSearchType,
} from "@/constants/category-search";

/**
 * 搜索工具栏分类
 */
export const useSearchStore = defineStore("category-search", {
  state: () => {
    return {
      // 分类列表
      categoryList: catSearchList,
      // 当前分类
      currentCategory: catSearchList[0] as catSearchType,
      currentItem: {} as catItemType,
    };
  },
  getters: {},
  actions: {
    initCurrentItem() {
      // if (Object.keys(this.currentItem).length!==0) return
      // 如果有子类就初始化第一个
      if (
        this.currentCategory?.children &&
        this.currentCategory.children.length > 0
      ) {
        this.currentItem = this.currentCategory.children[0];
      } else {
        // 没有子类，当前分类作为item
        // @ts-ignore
        this.currentItem = this.currentCategory;
      }
    },
    changeCurrentCategory(id: number) {
      const catId = this.categoryList.findIndex((item) => item.id === id);
      if (catId !== -1) {
        this.currentCategory = this.categoryList[catId];
      }
      // 改变分类后，初始化item为当前分类第一个
      this.initCurrentItem();
    },
    /**
     * 根据当前父类切换子类
     * @param title
     */
    changeCurrentItem(title: string) {
      // 如果没有子类，当前item为父类
      if (
        this.currentCategory?.children &&
        this.currentCategory.children.length > 0
      ) {
        const itemId = this.currentCategory.children.findIndex(
          (item: { title: string }) => item.title === title,
        );
        if (itemId !== -1) {
          // @ts-ignore
          this.currentItem = this.currentCategory.children[itemId];
        }

        return;
      }
      // @ts-ignore
      this.currentItem = this.currentCategory;
    },
  },
});
