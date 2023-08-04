export default {
  path: "/friend",
  meta: {
    title: "友情链接",
    icon: "fluent-mdl2:message-friend-request",
    rank: 50
  },
  component: () => import("@/views/friend/index.vue")
} as RouteConfigsTable;
