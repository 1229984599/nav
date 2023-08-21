import { RouteRecordRaw } from "vue-router";

const menuRoutes: RouteRecordRaw[] = [
  {
    name: "Menu",
    path: "/menu",
    redirect: "/menu/list",
    component: () => import("@/layout/index.vue"),
    children: [
      {
        name: "MenuList",
        path: "/menu/list",
        component: () => import("@/views/menu/index.vue"),
        meta: {
          title: "菜单管理",
          icon: "ep:menu",
        },
      },
    ],
  },
];
export default menuRoutes;
