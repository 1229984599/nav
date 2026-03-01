import Crud from "@/api/crud";
import { request } from "@/utils/request";
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

  async batchUpdate(data: Array<{ id: number; order: number }>): Promise<any> {
    return await request({
      method: "put",
      url: "/menu/update/all",
      data,
    });
  }
}

export default new Menu("/menu");
