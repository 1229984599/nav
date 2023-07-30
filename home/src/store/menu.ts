import { defineStore } from "pinia";
import menu from "@/api/menu";

/**
 * 记录分类和所有数据
 */
export const useMenuStore = defineStore("menu", {
  state: () => ({
    menuList: [],
    menuTree: [],
  }),
  actions: {
    async getMenuList() {
      const resp = await menu.list(1, 100);
      this.menuList = resp.items;
    },
    async getMenuTree() {
      // @ts-ignore
      this.menuTree = await menu.getMenuTree();
    },
  },
});
