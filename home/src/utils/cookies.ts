/** 统一处理 Cookie */

import CacheKey from "@/constants/cache-key";
import Cookies from "js-cookie";
import { LoginResponseData } from "@/api/login/types";

export const getToken = () => {
  return Cookies.get(CacheKey.TOKEN);
};
export const setToken = (token: LoginResponseData) => {
  Cookies.set(CacheKey.TOKEN, token.access_token, {
    expires: new Date(token.expires),
  });
};
export const removeToken = () => {
  Cookies.remove(CacheKey.TOKEN);
};
