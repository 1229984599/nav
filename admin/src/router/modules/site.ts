export default {
  path: "/site",
  meta: {
    title: "站点信息",
    icon: "dashicons:admin-site",
    rank: 10
  },
  component: () => import("@/views/site/index.vue")
} as RouteConfigsTable;
