import Crud from "@/api/crud";
import { PageUserSchemaList, UserSchemaFilters } from "./types";

class User extends Crud {
  /**
   * 获取列表
   * @param page
   * @param pageSize
   * @param filters
   */
  async list(
    page: number = 1,
    pageSize: number = 10,
    filters: UserSchemaFilters = {}
  ): Promise<PageUserSchemaList> {
    return await super.list(page, pageSize, filters);
  }
}

export default new User("/user");
