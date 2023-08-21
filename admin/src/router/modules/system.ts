import { RouteRecordRaw } from "vue-router";

const systemRoutes: RouteRecordRaw[] = [
  {
    name: "System",
    path: "/system",
    meta: {
      title: "系统管理",
      icon: "icon-park-outline:system",
    },
    redirect: "/system/user/list",
    component: () => import("@/layout/index.vue"),
    children: [
      {
        name: "User",
        path: "/system/user/list",
        meta: {
          title: "用户列表",
          icon: "mdi:user",
        },
        component: () => import("@/views/system/user/index.vue"),
      },
    ],
  },
];
export default systemRoutes;
