import { createApp } from "vue";
import "./styles/index.scss";
import "@/composables/useTheme"; // Apply dark mode class before first paint
import App from "./App.vue";
import { installPlugins } from "@/plugins";

const app = createApp(App);
installPlugins(app);
app.mount("#app");
