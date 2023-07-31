import Crud from "@/api/crud";
import { http } from "@/utils/http";

class Links extends Crud {
  /**
   * 获取列表
   * @param page
   * @param pageSize
   * @param filters
   */
  async list(
    page: number = 1,
    pageSize: number = 10,
    filters = {}
  ): Promise<any> {
    const resp = await http.post(`${this.baseUrl}/list`, {
      params: {
        page: page,
        size: pageSize
      },
      data: filters
    });
    // @ts-ignore
    resp.items.forEach(item => {
      item.menus = item.menus?.map(menu => menu.id);
    });
    return resp;
  }

  async create(data: any): Promise<any> {
    return await http.post(`${this.baseUrl}/menu/create`, { data });
  }

  /**
   * 更新
   * @param id
   * @param data
   */
  async update(id: number, data: any): Promise<any> {
    return await http.request("put", `${this.baseUrl}/menu/${id}`, { data });
  }

  async getSiteInfo(url: string) {
    return await http.post(`${this.baseUrl}/siteinfo?url=${url}`);
  }
}

export default new Links("/link");
