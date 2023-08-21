export interface LoginRequestData {
  username: string;
  /** 密码 */
  password: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  expires: string;
}
/**
 * UserRead
 */
export interface UserRead {
  /**
   * Created，创建时间
   */
  created?: Date;
  /**
   * Id
   */
  id?: number;
  /**
   * Nickname
   */
  nickname?: string;
  /**
   * Updated，更新时间
   */
  updated?: Date;
  /**
   * Username
   */
  username?: string;
}
