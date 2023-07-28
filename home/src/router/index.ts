import {
  createRouter,
  createWebHistory,
  Router,
  RouteRecordRaw,
} from "vue-router";
import { pcRoutes } from "@/router/pc";

export const systemRoutes: RouteRecordRaw[] = [];

const router: Router = createRouter({
  history: createWebHistory(),
  routes: [...systemRoutes, ...pcRoutes],
});

export default router;
