import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

// @ts-ignore
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export default pinia;
