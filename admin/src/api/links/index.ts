import Crud, { QueryParams } from "@/api/crud";
import { request } from "@/utils/request";
import {
  CreateMenuSchema,
  LinkSchemaList,
  LinksSchemaFilters,
  PageLinkSchemaList,
  SiteInfo,
} from "./types";

class Links extends Crud {
  async list(
    query: QueryParams = {},
    filters: LinksSchemaFilters = {},
  ): Promise<PageLinkSchemaList> {
    if (!query.order_by) {
      query.order_by = "order";
    }
    return await super.list(query, filters);
  }

  async getSiteInfo(url: string): Promise<SiteInfo> {
    return await request({
      method: "post",
      url: `${this.baseUrl}/siteinfo`,
      params: {
        url: url,
      },
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

  async createWithMenu(data: CreateMenuSchema): Promise<any> {
    return await request({
      url: `${this.baseUrl}/menu/create`,
      method: "post",
      data,
    });
  }
}

export default new Links("/links");
