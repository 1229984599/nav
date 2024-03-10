import { defineStore } from "pinia";

/**
 * 记录主题相关信息
 */
export const useAppStore = defineStore("app", {
  state: () => ({
    isCollapse: false,
  }),
  actions: {
    toggleSlide() {
      // debugger;
      this.isCollapse = !this.isCollapse;
    },
  },
});
