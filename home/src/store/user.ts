import { defineStore } from "pinia";

import { getToken, removeToken, setToken } from "@/utils/cookies";
import { loginApi, getUserinfoApi } from "@/api/login";
import { LoginRequestData } from "@/api/login/types";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: getToken() || "",
    username: "",
  }),
  actions: {
    async login(loginData: LoginRequestData) {
      const resp = await loginApi(loginData);
      this.username = loginData.username;
      setToken(resp);
      this.token = resp.access_token;
      await this.getUserinfo();
    },
    async getUserinfo() {
      const resp = await getUserinfoApi();
      this.username = <string>resp.username;
    },
    resetToken() {
      removeToken();
      this.token = "";
    },
    logout() {
      this.resetToken();
      this.username = "";
      location.reload();
    },
  },
  persist: {
    paths: ["username"],
  },
});
