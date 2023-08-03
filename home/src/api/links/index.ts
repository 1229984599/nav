import Crud from "@/api/crud";
import { request } from "@/utils/service";
import {
  CreateMenuSchema,
  LinkSchemaList,
  LinksSchemaFilters,
  PageLinkSchemaList,
  SiteInfo,
} from "./types";

class Links extends Crud {
  async list(
    page: number = 1,
    pageSize: number = 10,
    filters: LinksSchemaFilters = {},
  ): Promise<PageLinkSchemaList> {
    return await super.list(page, pageSize, filters);
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

export default new Links("/link");
