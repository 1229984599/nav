export default {
  path: "/links",
  meta: {
    title: "链接管理",
    icon: "zondicons:education"
  },
  component: () => import("@/views/links/index.vue")
} as RouteConfigsTable;
