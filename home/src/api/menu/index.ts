import Crud from "@/api/crud";
import { request } from "@/utils/service";
import {
  MenuSchemaFilters,
  MenuSchemaTree,
  PageMenuSchemaList,
} from "@/api/menu/types";

class Menu extends Crud {
  async list(
    query = {
      page: 1,
      pageSize: 10,
    },
    filters: MenuSchemaFilters = {},
  ): Promise<PageMenuSchemaList> {
    return await super.list(query, filters);
  }
  async getMenuTree(): Promise<MenuSchemaTree> {
    return await request({
      method: "get",
      url: "/menu/tree",
    });
  }
}

export default new Menu("/menu");
