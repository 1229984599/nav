import { defineStore } from "pinia";
import variable from "@/styles/variables.module.scss";
import { isMobile } from "@/utils/window";
import site from "@/api/site";

export const useAppStore = defineStore("app", {
  state: () => {
    return {
      isCollapse: false,
      cssVar: variable,
    };
  },
  actions: {
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    },
    changeBgColor(color: string) {
      // @ts-ignore
      this.cssVar.menuBg = color;
    },
    async clearCache() {
      return await site.clearCache();
    },
  },
  persist: {
    paths: ["isCollapse"],
  },
});
