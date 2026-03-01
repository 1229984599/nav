import { defineStore } from "pinia";
import { getRandImg } from "@/api/spider";

/**
 * 记录主题相关信息
 */
export const useAppStore = defineStore("app", {
  state: () => ({
    isCollapse: false,
    // 背景图片地址
    bgUrl: "https://api.nnxv.cn/api/Bing.php",
    isDark: false,
  }),
  actions: {
    toggleSlide() {
      this.isCollapse = !this.isCollapse;
    },
    async getRandomBg() {
      this.bgUrl = await getRandImg();
    },
    toggleDark() {
      this.isDark = !this.isDark;
      document.documentElement.classList.toggle("dark", this.isDark);
    },
    initDark() {
      document.documentElement.classList.toggle("dark", this.isDark);
    },
  },
  persist: {
    paths: ["isCollapse", "bgUrl", "isDark"],
  },
});
