import { RouteRecordRaw } from "vue-router";

const friendRoutes: RouteRecordRaw[] = [
  {
    name: "Friend",
    path: "/friend",
    redirect: "/friend/list",
    component: () => import("@/layout/index.vue"),
    children: [
      {
        name: "FriendList",
        path: "/friend/list",
        component: () => import("@/views/friend/index.vue"),
        meta: {
          title: "友情链接",
          icon: "fluent-mdl2:message-friend-request",
        },
      },
    ],
  },
];
export default friendRoutes;
