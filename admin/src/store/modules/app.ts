import { defineStore } from "pinia";
import variable from "@/styles/variables.module.scss";
import { isMobile } from "@/utils/window";
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
      this.cssVar.menuBg = color;
    },
  },
  persist: {
    paths: ["isCollapse"],
  },
});
