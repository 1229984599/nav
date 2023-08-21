import { App } from "vue";

import pinia from "./pinia";
import router from "@/router";
import { installElementPlus } from "./element-plus";
import { useFastCrud } from "@/plugins/fast-crud";

export function installPlugins(app: App) {
  app.use(router);
  app.use(pinia);
  installElementPlus(app);
  useFastCrud(app);
}
