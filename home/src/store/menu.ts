import { defineStore } from "pinia";
import menu from "@/api/menu";
import { MenuSchemaList, MenuSchemaTree } from "@/api/menu/types";

/**
 * 记录分类和所有数据
 */
export const useMenuStore = defineStore("menu", {
  state: () => ({
    menuList: new Array<MenuSchemaList>(),
    menuTree: new Array<MenuSchemaTree>(),
  }),
  actions: {
    async getMenuList() {
      const { items } = await menu.list(1, 100);
      this.menuList = items;
      return items;
    },
    async getMenuTree() {
      // @ts-ignore
      this.menuTree = await menu.getMenuTree();
      return this.menuTree;
    },
  },
});
