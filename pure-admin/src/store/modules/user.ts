import { defineStore } from "pinia";
import { store } from "@/store";
import { userType } from "./types";
import { routerArrays } from "@/layout/types";
import { router, resetRouter } from "@/router";
import { storageSession } from "@pureadmin/utils";
import { getLogin, refreshTokenApi, getUserInfo } from "@/api/login";
import { useMultiTagsStoreHook } from "@/store/modules/multiTags";
import {
  setToken,
  removeToken,
  sessionKey,
  setUserInfo
} from "@/utils/auth";
import { Token, UserSchemaLogin, UserSchemaRead } from "@/api/login/types";

export const useUserStore = defineStore({
  id: "pure-user",
  state: (): userType => ({
    // 用户名
    username:
      storageSession().getItem<UserSchemaRead>(sessionKey)?.username ?? "",
    // 页面级别权限
    roles: storageSession().getItem<UserSchemaRead>(sessionKey)?.roles ?? []
  }),
  actions: {
    /** 存储用户名 */
    SET_USERNAME(username: string) {
      this.username = username;
    },
    /** 存储角色 */
    SET_ROLES(roles: Array<string>) {
      this.roles = roles;
    },
    /** 登入 */
    async loginByUsername(data: UserSchemaLogin) {
      return new Promise<Token>((resolve, reject) => {
        getLogin(data)
          .then(async token => {
            setToken(token);
            const userInfo = await getUserInfo();
            setUserInfo(userInfo);
            // @ts-ignore
            resolve(token);
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    /** 前端登出（不调用接口） */
    logOut() {
      this.username = "";
      this.roles = [];
      removeToken();
      useMultiTagsStoreHook().handleTags("equal", [...routerArrays]);
      resetRouter();
      router.push("/login");
    },
    /** 刷新`token` */
    async handRefreshToken() {
      return new Promise<Token>((resolve, reject) => {
        refreshTokenApi()
          .then(token => {
            setToken(token);
            // @ts-ignore
            resolve(token);
          })
          .catch(error => {
            reject(error);
          });
      });
    }
  }
});

export function useUserStoreHook() {
  return useUserStore(store);
}
