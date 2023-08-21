import { createRouter, createWebHashHistory, Router } from "vue-router";
import { privateRoutes } from "@/router/private";
import { publicRoutes } from "@/router/public";

const router: Router = createRouter({
  history: createWebHashHistory(),
  routes: [...publicRoutes, ...privateRoutes],
});

export default router;
