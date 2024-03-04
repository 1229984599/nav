import Crud, { QueryParams } from "@/api/crud";
import { request } from "@/utils/request";
import { FriendSchemaFilters, PageFriendSchemaList, SiteInfo } from "./types";

class Friend extends Crud {
  async list(
    query: QueryParams = {},
    filters: FriendSchemaFilters = {},
  ): Promise<PageFriendSchemaList> {
    if (!query.order_by) {
      query.order_by = "order";
    }
    return await super.list(query, filters);
  }

  async getSiteInfo(url: string): Promise<SiteInfo> {
    return await request({
      url: `${this.baseUrl}/siteinfo?url=${url}`,
      method: "post",
    });
  }

  async syncCdn(url: string, link_id: any) {
    return await request({
      method: "post",
      url: `${this.baseUrl}/sync_cdn`,
      params: {
        url,
        link_id,
      },
    });
  }
}

export default new Friend("/friend");
