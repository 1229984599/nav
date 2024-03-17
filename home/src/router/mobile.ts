import { RouteRecordRaw } from "vue-router";

export const mobileRoutes: RouteRecordRaw[] = [
  {
    path: "/mobile",
    name: "Mobile",
    component: () => import("@/views/mobile/index.vue"),
  },
];
