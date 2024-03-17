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
  }),
  actions: {
    toggleSlide() {
      // debugger;
      this.isCollapse = !this.isCollapse;
    },
    async getRandomBg() {
      this.bgUrl = await getRandImg();
    },
  },
  persist: {
    paths: ["isCollapse", "bgUrl"],
  },
});
