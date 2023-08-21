import { RouteRecordRaw } from "vue-router";

/**
 * 公有路由
 */
export const publicRoutes: RouteRecordRaw[] = [
  {
    name: "home",
    path: "/",
    redirect: "/links",
    component: () => import("@/layout/index.vue"),
    children: [
      // {
      //   name: "home",
      //   path: "/home",
      //   meta: {
      //     title: "首页",
      //     icon: "material-symbols:home",
      //   },
      //   component: () => import("@/views/home/index.vue"),
      // },
      {
        name: "404",
        path: "/404",
        meta: {
          title: "404",
          hidden: true,
        },
        component: () => import("@/views/error-page/404.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/login/index.vue"),
  },
];
