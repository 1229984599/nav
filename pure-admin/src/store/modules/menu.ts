import { defineStore } from "pinia";
import menu from "@/api/menu";

/**
 * 记录分类和所有数据
 */
export const useMenuStore = defineStore("menu", {
  state: () => ({
    menuList: [],
    menuTree: []
  }),
  actions: {
    async getMenuList() {
      const { items } = await menu.list(1, 100);
      this.menuList = items;
      // return items?.map(item => item.id);
      return items;
    },
    async getMenuTree() {
      // @ts-ignore
      this.menuTree = await menu.getMenuTree();
    }
  }
});
