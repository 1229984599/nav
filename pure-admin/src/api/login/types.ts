/**
 * UserSchemaLogin
 */
export interface UserSchemaLogin {
  /**
   * Password，密码
   */
  password: string;
  /**
   * Username，用户名
   */
  username: string;
}

/**
 * Token
 */
export interface Token {
  /**
   * Access Token
   */
  access_token: string;
  /**
   * Expires
   */
  expires: Date;
  /**
   * Refresh Token
   */
  refresh_token: string;
}

/**
 * UserSchema
 */
interface UserSchema {
  /**
   * Created，创建时间
   */
  created?: Date | null;
  /**
   * Id
   */
  id: number;
  /**
   * Nickname
   */
  nickname?: null | string;
  /**
   * Updated，更新时间
   */
  updated?: Date | null;
  /**
   * Username，用户名
   */
  username: string;
}

export interface UserSchemaRead extends UserSchema {
  roles?: string[];
}

export interface UserRead extends UserSchema {
  roles?: RoleSchemaRelation[];
}

/**
 * RoleSchemaRelation
 */
export interface RoleSchemaRelation {
  /**
   * Id
   */
  id: number;
  /**
   * Name，角色名称：roleManager
   */
  name: string;
  /**
   * Title，角色标题：用户管理员
   */
  title: string;
}
