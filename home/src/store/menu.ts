import { defineStore } from "pinia";
import menu from "@/api/menu";
import { MenuSchemaTree } from "@/api/menu/types";
import { LinkSchemaList } from "@/api/links/types";

/**
 * 记录分类和所有数据
 */
export const useMenuStore = defineStore("menu", {
  state: () => ({
    menuTree: new Array<MenuSchemaTree>(),
    localMenu: {
      color: "#C71585",
      icon: "ion:bookmarks",
      title: "本地书签",
      status: true,
      links: new Array<LinkSchemaList>(),
    } as MenuSchemaTree,
  }),
  actions: {
    async getMenuTree() {
      // @ts-ignore
      this.menuTree = await menu.getMenuTree();
      return this.menuTree;
    },
    // 添加编辑一起，有就覆盖，没有就添加
    addLocalLink(link: LinkSchemaList) {
      const index = this.localMenu.links?.findIndex(
        (item) => item.href === link.href,
      );
      // 如果没有就添加
      if (index === -1) {
        this.localMenu.links?.push(link);
      }
      // 否则就覆盖
      // @ts-ignore
      this.localMenu.links[index] = link;
    },
    deleteLocalLink(link: LinkSchemaList) {
      const index = this.localMenu.links?.findIndex(
        (item) => item.href === link.href,
      );
      if (index !== -1) {
        //@ts-ignore
        this.localMenu.links?.splice(index, 1);
      }
      return;
    },
    // 清空本地书签
    resetLocalLink() {
      this.localMenu.links = [];
    },
  },
  persist: {
    paths: ["menuTree", "localMenu"],
  },
});
