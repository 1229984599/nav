import { ConfigEnv, defineConfig, loadEnv, UserConfigExport } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";
import path from "path";

// https://vitejs.dev/config/
export default (configEnv: ConfigEnv): UserConfigExport => {
  const viteEnv = loadEnv(configEnv.mode, process.cwd());
  const { VITE_PUBLIC_PATH, VITE_BASE_API } = viteEnv;
  return defineConfig({
    define: {
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "true",
    },
    base: VITE_PUBLIC_PATH,
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: true,
      port: 3000,
      cors: true,
      proxy: {
        "/api": {
          target: VITE_BASE_API,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
        "/hotapi": {
          target: "https://api.gumengya.com/Api/",
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/hotapi/, ""),
        },
      },
    },
    plugins: [vue(), vueJsx()],
  });
};
