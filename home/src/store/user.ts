import { defineStore } from "pinia";

import { loginApi, getUserinfoApi } from "@/api/login";
import { LoginRequestData, Token, UserRead } from "@/api/login/types";

const SOY_TOKEN_KEY = "SOY_token";
const SOY_REFRESH_TOKEN_KEY = "SOY_refreshToken";

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
      // Sync token to admin app for SSO
      this.syncTokenToAdmin();
    },
    async getUserinfo(options?: { silent?: boolean }) {
      const userInfo = await getUserinfoApi(options);
      this.userInfo = userInfo;
      this.sessionVerified = !!userInfo?.id;
    },
    /** Sync token to admin app's localStorage format (SOY_ prefix, JSON.stringify wrapped) */
    syncTokenToAdmin() {
      if (this.token?.access_token) {
        localStorage.setItem(SOY_TOKEN_KEY, JSON.stringify(this.token.access_token));
      }
      if (this.token?.refresh_token) {
        localStorage.setItem(SOY_REFRESH_TOKEN_KEY, JSON.stringify(this.token.refresh_token));
      }
    },
    /** Try to read token from admin app's localStorage if home has no valid token */
    syncFromAdmin() {
      if (this.hasValidToken) return;
      const raw = localStorage.getItem(SOY_TOKEN_KEY);
      if (!raw) return;
      // Admin uses JSON.stringify when storing, so unwrap it
      let adminToken: string;
      try {
        adminToken = JSON.parse(raw);
      } catch {
        adminToken = raw; // fallback: raw string (legacy format)
      }
      if (adminToken && typeof adminToken === 'string') {
        let refreshToken = '';
        const rawRefresh = localStorage.getItem(SOY_REFRESH_TOKEN_KEY);
        if (rawRefresh) {
          try { refreshToken = JSON.parse(rawRefresh); } catch { refreshToken = rawRefresh; }
        }
        const expires = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
        this.token = { access_token: adminToken, refresh_token: refreshToken, expires };
      }
    },
    async verifyAdminSession() {
      // Try syncing from admin first if we don't have a valid token
      this.syncFromAdmin();

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
          await this.getUserinfo({ silent: true });
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
      // Clear admin app's storage too for SSO logout
      localStorage.removeItem(SOY_TOKEN_KEY);
      localStorage.removeItem(SOY_REFRESH_TOKEN_KEY);
      location.reload();
    },
  },
  persist: {
    paths: ["token", "userInfo"],
  },
});
