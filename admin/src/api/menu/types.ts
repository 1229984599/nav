import { LinkSchemaList } from "@/api/links/types";

/**
 * Page_MenuSchemaList_
 */
export interface PageMenuSchemaList {
  /**
   * Items
   */
  items: MenuSchemaList[];
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
 * MenuSchemaList
 */
export interface MenuSchemaList {
  /**
   * Color，图标颜色hex
   */
  color?: string;
  /**
   * Created，创建时间
   */
  create_time?: Date;
  /**
   * Icon，图标字符串
   */
  icon?: string;
  /**
   * Id
   */
  id?: number;
  /**
   * Links
   */
  links: LinkSchemaList[];
  /**
   * Order，值越大越靠前
   */
  order?: number;
  /**
   * Parent Id
   */
  parent_id?: number;
  /**
   * Title
   */
  title?: string;
  /**
   * Updated，更新时间
   */
  update_time?: Date;
}

export interface MenuSchemaTree {
  id?: number;
  parent_id?: number;
  title?: string;
  icon?: string;
  color?: string;
  links?: LinkSchemaList[];
  children?: MenuSchemaTree[];
}
/**
 * MenuSchemaFilters
 */
export interface MenuSchemaFilters {
  /**
   * Title
   */
  title?: string;
  parent_id?: number;
}
