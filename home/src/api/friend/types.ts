export interface SiteInfo {
  title?: string;
  icon?: string;
  desc?: string;
}
/**
 * FriendSchemaFilters
 */
export interface FriendSchemaFilters {
  /**
   * Title
   */
  title?: string;
}
/**
 * Page_FriendSchemaList_
 */
export interface PageFriendSchemaList {
  /**
   * Items
   */
  items: FriendSchemaList[];
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
 * FriendSchemaList
 */
export interface FriendSchemaList {
  /**
   * Color，图标颜色hex
   */
  color?: null | string;
  /**
   * Created，创建时间
   */
  created?: Date | null;
  /**
   * Desc
   */
  desc?: null | string;
  /**
   * Href
   */
  href?: string;
  /**
   * Icon
   */
  icon?: null | string;
  /**
   * Id
   */
  id?: number;
  /**
   * Order，值越大越靠前
   */
  order?: number | null;
  /**
   * Title
   */
  title?: string;
  /**
   * Updated，更新时间
   */
  updated?: Date | null;
}
