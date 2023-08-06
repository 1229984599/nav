const Layout = () => import("@/layout/index.vue");

export default {
  path: "/",
  name: "Home",
  component: Layout,
  redirect: "/menu",
  meta: {
    icon: "homeFilled",
    title: "首页",
    rank: 0,
    showLink: false
  },
  children: [
    {
      path: "/welcome",
      name: "Welcome",
      component: () => import("@/views/welcome/index.vue"),
      meta: {
        title: "首页"
      }
    }
  ]
} as RouteConfigsTable;
