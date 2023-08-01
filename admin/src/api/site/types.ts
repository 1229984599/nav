/**
 * SiteSchemaCreate
 */
export interface SiteSchema {
  id?: null | Number;
  /**
   * Color，图标颜色hex
   */
  color?: null | string;
  /**
   * Desc，站点描述
   */
  desc?: null | string;
  /**
   * Footer，底部版权信息等
   */
  footer?: null | string;
  /**
   * Icon，图标地址
   */
  icon?: null | string;
  /**
   * Keywords，站点关键字
   */
  keywords?: null | string;
  /**
   * Title，网站标题
   */
  title?: string;
}
