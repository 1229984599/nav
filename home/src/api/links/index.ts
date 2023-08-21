import Crud from "@/api/crud";
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
    query = {
      page: 1,
      pageSize: 10,
      order_by: "-create_time",
    },
    filters: LinksSchemaFilters = {},
  ): Promise<PageLinkSchemaList> {
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

  async createWithMenu(data: CreateMenuSchema): Promise<any> {
    return await request({
      url: `${this.baseUrl}/menu/create`,
      method: "post",
      data,
    });
  }
}

export default new Links("/links");
