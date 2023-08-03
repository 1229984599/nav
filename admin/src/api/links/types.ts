/**
 * Page_LinkSchemaList_
 */
export interface PageLinkSchemaList {
  /**
   * Items
   */
  items: LinkSchemaList[];
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
 * LinkSchemaList
 */
export interface LinkSchemaList {
  /**
   * Color，图标颜色hex
   */
  color?: string;
  /**
   * Created，创建时间
   */
  created?: Date;
  /**
   * Desc
   */
  desc?: string;
  /**
   * Href
   */
  href?: string;
  /**
   * Icon
   */
  icon?: string;
  /**
   * Id
   */
  id?: number;
  /**
   * Is Self
   */
  is_self?: boolean;
  /**
   * Menus
   */
  menus: MenuSchemaRelation[];
  /**
   * Order，值越大越靠前
   */
  order?: number;
  /**
   * Title
   */
  title?: string;
  /**
   * Updated，更新时间
   */
  updated?: Date;
}

/**
 * MenuSchemaRelation
 */
export interface MenuSchemaRelation {
  /**
   * Id
   */
  id?: number;
  /**
   * Title
   */
  title?: string;
}

/**
 * SiteInfo
 */
export interface SiteInfo {
  title?: string;
  icon?: string;
  desc?: string;
}
/**
 * LinksSchemaFilters
 */
export interface LinksSchemaFilters {
  /**
   * Title
   */
  title?: string;
}
/**
 * CreateMenuSchema
 */
export interface CreateMenuSchema {
  /**
   * Color，图标颜色hex
   */
  color?: string;
  /**
   * Desc
   */
  desc?: string;
  /**
   * Href
   */
  href?: string;
  /**
   * Icon
   */
  icon?: string;
  /**
   * Is Self
   */
  is_self?: boolean;
  /**
   * Menus
   */
  menus?: number[];
  /**
   * Order，值越大越靠前
   */
  order?: number | null;
  /**
   * Title
   */
  title?: string;
}
