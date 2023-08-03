import Crud from "@/api/crud";
import { request } from "@/utils/service";
import { FriendSchemaFilters, PageFriendSchemaList, SiteInfo } from "./types";

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
    filters: FriendSchemaFilters = {},
  ): Promise<PageFriendSchemaList> {
    return await super.list(page, pageSize, filters);
  }

  async getSiteInfo(url: string): Promise<SiteInfo> {
    return await request({
      url: `${this.baseUrl}/siteinfo?url=${url}`,
      method: "GET",
    });
  }
}

export default new Friend("/friend");
