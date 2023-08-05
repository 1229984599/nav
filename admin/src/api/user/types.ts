/**
 * Page_UserSchemaList_
 */
export interface PageUserSchemaList {
  /**
   * Items
   */
  items: UserSchemaList[];
  /**
   * Page
   */
  page?: number;
  /**
   * Pages
   */
  pages?: number;
  /**
   * Size
   */
  size?: number;
  /**
   * Total
   */
  total: number;
}

/**
 * UserSchemaList
 */
export interface UserSchemaList {
  /**
   * Created，创建时间
   */
  created?: Date | null;
  /**
   * Id
   */
  id?: number;
  /**
   * Nickname
   */
  nickname?: null | string;
  /**
   * Password
   */
  password?: string;
  /**
   * Updated，更新时间
   */
  updated?: Date | null;
  /**
   * Username
   */
  username?: string;
}
/**
 * UserSchemaFilters
 */
export interface UserSchemaFilters {
  /**
   * Username
   */
  username?: string;
}
