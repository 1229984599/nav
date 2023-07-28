import Crud from "@/api/crud";
import { request } from "@/utils/service";

class Menu extends Crud {
  async getMenuTree() {
    return await request({
      method: "get",
      url: "/menu/tree",
    });
  }
}

export default new Menu("/menu");
