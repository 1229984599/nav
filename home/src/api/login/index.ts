import { request } from "@/utils/request";
import { LoginRequestData, LoginResponseData, UserRead } from "./types";

/** 登录并返回 Token */
export function loginApi(data: LoginRequestData) {
  return request<LoginResponseData>({
    url: "system/login/login",
    method: "post",
    data,
  });
}

// 获取个人信息
export function getUserinfoApi() {
  return request<UserRead>({
    url: "system/login/me",
    method: "get",
  });
}
