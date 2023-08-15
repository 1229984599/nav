import { request } from "@/utils/service";
import { LoginRequestData, LoginResponseData, UserRead } from "./types";

/** 登录并返回 Token */
export function loginApi(data: LoginRequestData) {
  return request<LoginResponseData>({
    url: "login/login",
    method: "post",
    data,
  });
}

// 获取个人信息
export function getUserinfoApi() {
  return request<UserRead>({
    url: "login/user/me",
    method: "get",
  });
}
