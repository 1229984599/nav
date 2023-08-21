import Crud, { QueryParams } from "@/api/crud";
import { PageUserSchemaList, UserSchemaFilters } from "./types";

class User extends Crud {
  /**
   * 获取列表
   * @param queryParams
   * @param filters
   */
  async list(
    queryParams: QueryParams={},
    filters: UserSchemaFilters = {},
  ): Promise<PageUserSchemaList> {
    return await super.list(queryParams, filters);
  }
}

export default new User("/system/user");
