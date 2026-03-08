import { defineStore } from "pinia";
import menu from "@/api/menu";
import { MenuSchemaTree } from "@/api/menu/types";

/**
 * 记录分类和所有数据
 */
export const useMenuStore = defineStore("menu", {
  state: () => ({
    menuTree: new Array<MenuSchemaTree>(),
    // 用于侧边栏点击子分类时通知 TabCategory 切换到对应 tab
    activeSubTab: null as { parentId: number; childId: number } | null,
    // 侧边栏当前高亮的菜单 index（与页面 tab 联动）
    activeMenuIndex: "",
  }),
  actions: {
    async getMenuTree() {
      // @ts-ignore
      this.menuTree = await menu.getMenuTree();
      return this.menuTree;
    },
    setActiveSubTab(parentId: number, childId: number) {
      this.activeSubTab = { parentId, childId };
    },
    clearActiveSubTab() {
      this.activeSubTab = null;
    },
    setActiveMenuIndex(index: string) {
      this.activeMenuIndex = index;
    },
  },
});
