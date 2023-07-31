export default {
  path: "/menu",
  meta: {
    title: "菜单管理",
    icon: "zondicons:education"
  },
  component: () => import("@/views/menu/index.vue")
} as RouteConfigsTable;
