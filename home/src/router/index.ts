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
  routes: [
    ...systemRoutes,
    ...pcRoutes,
    ...mobileRoutes,
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      redirect: "/list",
    },
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return false;
  },
});

router.beforeEach((to, _from, next) => {
  // Frontend always stays on the PC view now.
  if (to.path === "/mobile") {
    return next({ path: "/list", replace: true });
  }
  next();
});

export default router;
