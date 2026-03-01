import { App } from "vue";

import pinia from "./pinia";
import router from "@/router";
import "./element-plus";

export function installPlugins(app: App) {
  app.use(router);
  app.use(pinia);
}
