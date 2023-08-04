import { defineStore } from "pinia";
import menu from "@/api/menu";
import { MenuSchemaTree } from "@/api/menu/types";

/**
 * 记录分类和所有数据
 */
export const useMenuStore = defineStore("menu", {
  state: () => ({
    menuTree: new Array<MenuSchemaTree>(),
  }),
  actions: {
    async getMenuTree() {
      // @ts-ignore
      this.menuTree = await menu.getMenuTree();
      return this.menuTree;
    },
  },
});
