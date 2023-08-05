import { defineStore } from "pinia";

import { getToken, removeToken, setToken } from "@/utils/cookies";
import { loginApi } from "@/api/login";
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
});
