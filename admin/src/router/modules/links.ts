export default {
  path: "/links",
  meta: {
    title: "链接管理",
    icon: "pajamas:link",
    rank: 10
  },
  component: () => import("@/views/links/index.vue")
} as RouteConfigsTable;
