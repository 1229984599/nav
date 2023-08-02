import Crud from "@/api/crud";
import { http } from "@/utils/http";

class Menu extends Crud {
  async getMenuTree() {
    return await http.get("/menu/tree");
  }
}

export default new Menu("/menu");
