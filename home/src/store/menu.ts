import { defineStore } from "pinia";
import menu from "@/api/menu";

/**
 * 记录分类和所有数据
 */
export const useMenuStore = defineStore("menu", {
  state: () => ({
    menuList: [],
  }),
  actions: {
    async getMenuList() {
      // @ts-ignore
      this.menuList = await menu.getMenuTree();
    },
  },
});
