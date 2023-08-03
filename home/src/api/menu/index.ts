import Crud from "@/api/crud";
import { request } from "@/utils/service";
import {
  MenuSchemaFilters,
  MenuSchemaTree,
  PageMenuSchemaList,
} from "@/api/menu/types";

class Menu extends Crud {
  async list(
    page: number = 1,
    pageSize: number = 10,
    filters: MenuSchemaFilters = {},
  ): Promise<PageMenuSchemaList> {
    return await super.list(page, pageSize, filters);
  }
  async getMenuTree(): Promise<MenuSchemaTree> {
    return await request({
      method: "get",
      url: "/menu/tree",
    });
  }
}

export default new Menu("/menu");
