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
}

export default new Nav("/nav");
