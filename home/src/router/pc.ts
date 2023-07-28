import { RouteRecordRaw } from "vue-router";

export const pcRoutes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/list",
    component: () => import("@/views/pc/index.vue"),
    children: [
      {
        path: "/list",
        component: () => import("@/views/pc/pages/list.vue"),
        name: "AppMain",
      },
    ],
  },
];
