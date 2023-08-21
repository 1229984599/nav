import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import { App } from "vue";

export function installElementPlus(app: App) {
  app.use(ElementPlus);
}
