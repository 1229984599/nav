import Crud, {QueryParams} from "@/api/crud";
import { request } from "@/utils/request";
import {
  MenuSchemaFilters,
  MenuSchemaTree,
  PageMenuSchemaList,
} from "@/api/menu/types";

class Menu extends Crud {
  async list(
    query:QueryParams={},
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
