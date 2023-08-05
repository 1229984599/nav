export interface LoginRequestData {
  /** admin 或 editor */
  username: "admin" | "editor";
  /** 密码 */
  password: string;
}

export interface LoginResponseData {
  access_token: string;
  refresh_token: string;
  expires: string;
}
