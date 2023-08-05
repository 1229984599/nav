export default {
  path: "/user",
  meta: {
    title: "用户管理",
    icon: "clarity:user-solid",
    rank: 30
  },
  component: () => import("@/views/user/index.vue")
} as RouteConfigsTable;
