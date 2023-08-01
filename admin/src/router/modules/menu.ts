export default {
  path: "/menu",
  meta: {
    title: "菜单管理",
    icon: "ep:menu",
    rank: 0
  },
  component: () => import("@/views/menu/index.vue")
} as RouteConfigsTable;
