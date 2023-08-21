import { RouteRecordRaw } from "vue-router";

const linksRoutes: RouteRecordRaw[] = [
  {
    name: "Links",
    path: "/links",
    redirect: "/links/list",
    component: () => import("@/layout/index.vue"),
    children: [
      {
        name: "LinkList",
        path: "/links/list",
        component: () => import("@/views/links/index.vue"),
        meta: {
          title: "链接管理",
          icon: "pajamas:link",
        },
      },
    ],
  },
];
export default linksRoutes;
