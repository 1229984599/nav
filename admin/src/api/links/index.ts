import Crud from "@/api/crud"
import { request } from "@/utils/service"

class Links extends Crud {
  async getSiteInfo(url: string) {
    return request({
      method: "post",
      url: `${this.baseUrl}/siteinfo`,
      params: {
        url: url
      }
    })
  }

  async createWithMenu(data: any): Promise<any> {
    return await request({
      url: `${this.baseUrl}/create_menu`,
      method: "post",
      data
    })
  }
}

export default new Links("/link")
