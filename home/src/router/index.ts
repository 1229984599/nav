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

// Auto-redirect mobile devices on initial load
const pcPaths = new Set(["/", "/list", "/search"]);
let isFirstNavigation = true;

router.beforeEach((to, _from, next) => {
  if (!isFirstNavigation) return next();
  isFirstNavigation = false;

  const isMobileDevice = window.innerWidth < 768;

  if (isMobileDevice && pcPaths.has(to.path)) {
    return next({ name: "Mobile" });
  }
  if (!isMobileDevice && to.path === "/mobile") {
    return next({ path: "/list" });
  }
  next();
});

export default router;
