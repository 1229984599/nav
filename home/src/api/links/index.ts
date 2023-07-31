import Crud from "@/api/crud";
import { request } from "@/utils/service";

class Nav extends Crud {
  async getSiteInfo(url: string) {
    return request({
      method: "post",
      url: `${this.baseUrl}/siteinfo`,
      params: {
        url: url,
      },
    });
  }
  async createWithMenu(data: any): Promise<any> {
    return await request({
      url: `${this.baseUrl}/menu/create`,
      method: "post",
      data,
    });
  }
}

export default new Nav("/link");
