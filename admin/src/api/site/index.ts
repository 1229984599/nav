import { http } from "@/utils/http";
import { SiteSchema } from "./types";

class Site {
  async get(): Promise<SiteSchema> {
    return await http.get("/site/get");
  }
  async update(data: SiteSchema): Promise<boolean> {
    return await http.post("/site/update", { data });
  }
}
export default new Site();
