import { defineStore } from "pinia";
import { SiteSchema } from "@/api/site/types";
import siteModel from "@/api/site";

/**
 * 站点信息
 */
export const useSiteStore = defineStore("siteInfo", {
  state: () => ({
    siteInfo: Object as SiteSchema,
  }),
  actions: {
    async getSiteInfo() {
      this.siteInfo = await siteModel.get();
      return this.siteInfo;
    },
    async updateSiteInfo(data: SiteSchema) {
      this.siteInfo = await siteModel.update(data);
      return this.siteInfo;
    },
  },
  persist: true,
});
