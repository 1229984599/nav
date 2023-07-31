import { http } from "@/utils/http";
import { Token, UserSchemaLogin, UserRead } from "./types";
import { formatToken, getToken } from "@/utils/auth";

export const getLogin = (data?: UserSchemaLogin) => {
  return http.request<Token>("post", "/login/login", { data });
};

/** 刷新token */
export const refreshTokenApi = () => {
  const token = getToken();
  return http.request<Token>("post", "/login/refresh", {
    headers: {
      Authorization: formatToken(token.refresh_token)
    }
  });
};

export const getUserInfo = () => {
  return http.request<UserRead>("get", "/login/users/me");
};
