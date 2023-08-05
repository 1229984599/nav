import { request } from "@/utils/service";
import { LoginRequestData, LoginResponseData } from "./types";

/** 登录并返回 Token */
export function loginApi(data: LoginRequestData) {
  return request<LoginResponseData>({
    url: "login/login",
    method: "post",
    data,
  });
}
