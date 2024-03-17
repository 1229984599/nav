import {
  createRouter,
  createWebHistory,
  Router,
  RouteRecordRaw,
} from "vue-router";
import { pcRoutes } from "@/router/pc";
import { mobileRoutes } from "@/router/mobile";

export const systemRoutes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/login/index.vue"),
  },
];

const router: Router = createRouter({
  history: createWebHistory(),
  routes: [...systemRoutes, ...pcRoutes, ...mobileRoutes],
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        top: 0,
        behavior: "smooth",
      };
    }
  },
});

export default router;
