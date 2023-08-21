import Crud, {QueryParams} from "@/api/crud";
import { request } from "@/utils/request";
import { FriendSchemaFilters, PageFriendSchemaList, SiteInfo } from "./types";

class Friend extends Crud {
  async list(
    query:QueryParams={},
    filters: FriendSchemaFilters = {},
  ): Promise<PageFriendSchemaList> {
    return await super.list(query, filters);
  }

  async getSiteInfo(url: string): Promise<SiteInfo> {
    return await request({
      url: `${this.baseUrl}/siteinfo?url=${url}`,
      method: "GET",
    });
  }
}

export default new Friend("/friend");
