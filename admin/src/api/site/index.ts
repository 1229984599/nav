import { request } from "@/utils/request";
import { SiteSchema } from "./types";

class Site {
  async get(): Promise<SiteSchema> {
    return await request({
      url: "/site/get",
      method: "get",
    });
  }

  async update(data: SiteSchema): Promise<SiteSchema> {
    return await request({
      url: "/site/update",
      method: "post",
      data,
    });
  }
}

export default new Site();
