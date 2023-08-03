import Crud from "@/api/crud";
import { http } from "@/utils/http";
import { SiteInfo } from "./types";

class Friend extends Crud {
  /**
   * 获取列表
   * @param page
   * @param pageSize
   * @param filters
   */
  async list(
    page: number = 1,
    pageSize: number = 10,
    filters = {}
  ): Promise<any> {
    return await super.list(page, pageSize, filters);
  }

  async getSiteInfo(url: string): Promise<SiteInfo> {
    return await http.post(`${this.baseUrl}/siteinfo?url=${url}`);
  }
}

export default new Friend("/friend");
