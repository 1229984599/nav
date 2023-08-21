import { RouteRecordRaw } from "vue-router";

const siteRoutes: RouteRecordRaw[] = [
  {
    name: "site",
    path: "/site",
    redirect: "/site/list",
    component: () => import("@/layout/index.vue"),
    children: [
      {
        name: "siteList",
        path: "/site/list",
        component: () => import("@/views/site/index.vue"),
        meta: {
          title: "站点管理",
          icon: "dashicons:admin-site",
        },
      },
    ],
  },
];
export default siteRoutes;
