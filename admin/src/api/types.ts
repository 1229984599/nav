export interface BaseApiOut {
  /**
   * Code
   */
  code?: number;
  /**
   * Data
   */
  data?: any;
  /**
   * Message
   */
  message?: string;
}

/**
 * ItemListSchema[PermissionList]，数据查询返回格式
 */
export interface ItemListSchema<T> {
  items: T[];
  /**
   * Page
   */
  page: number;
  /**
   * Pages
   */
  pages?: number;
  /**
   * Size
   */
  size: number;
  /**
   * Total
   */
  total: number;
}
