import { createApp } from "vue";
import "./styles/index.scss";
import App from "./App.vue";
import { installPlugins } from "./plugins";
import "@/router/permission";

const app = createApp(App);
installPlugins(app);
app.mount("#app");
