import router from "@/router/index";
import { useUserStore } from "@/store";
import { NavigationGuardNext, RouteLocationNormalized } from "vue-router";

// 白名单
const whiteList = ["/login"];
/**
 * 路由前置守卫
 */

// 判断是否登录
router.beforeEach(
  async (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext,
  ) => {
    // 存在 token ，进入主页
    // if (store.state.user.token) {
    // 快捷访问
    const userStore = useUserStore();
    if (userStore.token?.access_token) {
      if (to.name === "Login") {
        console.log("已登录，直接进入主页");
        next("/");
      } else {
        if (!userStore.hasUserInfo) {
          console.log("获取用户信息");
          await userStore.getUserinfo();
        }
        next();
      }
    } else {
      // 没有token的情况下，可以进入白名单
      if (whiteList.indexOf(to.path) > -1) {
        next();
      } else {
        next({ name: "Login" });
      }
    }
  },
);
