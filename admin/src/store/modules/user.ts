import { defineStore } from "pinia";

import { loginApi, getUserinfoApi } from "@/api/system/login";
import { LoginRequestData, Token, UserRead } from "@/api/system/login/types";
import router from "@/router";
import { useTagsViewStore } from "@/store";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: {} as Token,
    userInfo: {} as UserRead,
  }),
  getters: {
    hasUserInfo(): boolean {
      return !!this.userInfo.id;
    },
  },
  actions: {
    async login(loginData: LoginRequestData) {
      this.userInfo = loginData;
      this.token = await loginApi(loginData);
    },
    async getUserinfo() {
      this.userInfo = await getUserinfoApi();
    },
    resetToken() {
      this.token = { access_token: "", expires: "", refresh_token: "" };
    },
    logout() {
      this.resetToken();
      this.userInfo = {};
      router.push({ name: "Login" });
      useTagsViewStore().tagsViewList = [];
    },
  },
  persist: {
    paths: ["token", "userInfo"],
  },
});
