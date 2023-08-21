import { request } from "@/utils/request";
import { LoginRequestData, Token, UserRead } from "./types";

/** 登录并返回 Token */
export async function loginApi(data: LoginRequestData): Promise<Token> {
  return request({
    url: "system/login/login",
    method: "post",
    data,
  });
}

// 获取个人信息
export async function getUserinfoApi(): Promise<UserRead> {
  return request({
    url: "system/login/me",
    method: "get",
  });
}
