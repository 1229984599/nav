import { defineStore } from "pinia";

import { loginApi, getUserinfoApi } from "@/api/login";
import { LoginRequestData, Token, UserRead } from "@/api/login/types";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: {} as Token,
    userInfo: {} as UserRead,
    sessionVerified: false,
    sessionVerifyPromise: null as Promise<boolean> | null,
  }),
  getters: {
    hasUserInfo(): boolean {
      return !!this.userInfo.id;
    },
    hasValidToken(): boolean {
      return !!this.token?.access_token && !!this.token?.expires && new Date(this.token.expires) > new Date();
    },
    isAdminAuthorized(): boolean {
      return this.sessionVerified && this.hasValidToken && !!this.userInfo.id;
    },
  },
  actions: {
    async login(loginData: LoginRequestData) {
      this.token = await loginApi(loginData);
      await this.getUserinfo();
    },
    async getUserinfo() {
      const userInfo = await getUserinfoApi();
      this.userInfo = userInfo;
      this.sessionVerified = !!userInfo?.id;
    },
    async verifyAdminSession() {
      if (!this.hasValidToken) {
        this.resetToken();
        this.userInfo = {};
        return false;
      }
      if (this.sessionVerified && this.hasUserInfo) {
        return true;
      }
      if (this.sessionVerifyPromise) {
        return this.sessionVerifyPromise;
      }
      this.sessionVerifyPromise = (async () => {
        try {
          await this.getUserinfo();
          return this.isAdminAuthorized;
        } catch {
          this.resetToken();
          this.userInfo = {};
          return false;
        } finally {
          this.sessionVerifyPromise = null;
        }
      })();
      try {
        return await this.sessionVerifyPromise;
      } finally {
        this.sessionVerifyPromise = null;
      }
    },
    resetToken() {
      this.token = { access_token: "", expires: "", refresh_token: "" };
      this.sessionVerified = false;
      this.sessionVerifyPromise = null;
    },
    logout() {
      this.resetToken();
      this.userInfo = {};
      location.reload();
    },
  },
  persist: {
    paths: ["token", "userInfo"],
  },
});
