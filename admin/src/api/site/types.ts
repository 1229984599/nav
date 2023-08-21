/**
 * SiteSchemaCreate
 */
export interface SiteSchema {
  id?: number | null;
  /**
   * Color，图标颜色hex
   */
  color?: string;
  /**
   * Desc，站点描述
   */
  desc?: string;
  /**
   * Footer，底部版权信息等
   */
  footer?: string;
  /**
   * Icon，图标地址
   */
  icon?: string;
  /**
   * Keywords，站点关键字
   */
  keywords?: string;
  /**
   * Title，网站标题
   */
  title?: string;
}
