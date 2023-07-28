import { createApp } from "vue";
import "./styles/index.scss";
import App from "./App.vue";
import { installPlugins } from "@/plugins";

const app = createApp(App);
installPlugins(app);
app.mount("#app");
