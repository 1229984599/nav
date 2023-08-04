import {
  createRouter,
  createWebHashHistory,
  Router,
  RouteRecordRaw,
} from "vue-router";
import { pcRoutes } from "@/router/pc";

export const systemRoutes: RouteRecordRaw[] = [];

const router: Router = createRouter({
  history: createWebHashHistory(),
  routes: [...systemRoutes, ...pcRoutes],
});

export default router;
