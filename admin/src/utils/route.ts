import { RouteRecordRaw } from "vue-router";
import path from "path-browserify";

/***
 * 获取所有路由（包括子路由）：打平
 * @param routes
 */
export const getAllRoutes = (routes: RouteRecordRaw[]): RouteRecordRaw[] => {
  const routeList: RouteRecordRaw[] = [];
  routes.forEach((route) => {
    if (route.children && route.children.length > 0) {
      routeList.push(...route.children);
      route.children = [];
    }
    routeList.push(route);
  });
  return routeList;
};

/***
 * 获取所有子路由
 * @param routes
 */
export const getChildrenRoutes = (
  routes: RouteRecordRaw[],
): RouteRecordRaw[] => {
  const routeList: RouteRecordRaw[] = [];
  routes.forEach((route) => {
    if (route.children && route.children.length > 0) {
      routeList.push(...route.children);
    }
  });
  return routeList;
};

/***
 * 过滤掉在子路由出现过的路由
 * @param routes
 */
export const filterRoutes = (routes: RouteRecordRaw[]): RouteRecordRaw[] => {
  const childrenRoutes = getChildrenRoutes(routes);
  return routes.filter((route) => {
    return !childrenRoutes.find((childrenRoute) => {
      // 如果当前路由和子路由path相同
      return childrenRoute.path === route.path;
    });
  });
};

export const isNull = (data: any): boolean => {
  if (!data) return true;
  return ["{}", "[]"].includes(JSON.stringify(data));
};

/***
 * 生成路由菜单
 * @param routes
 * @param basePath
 */
export const generateMenus = (
  routes: RouteRecordRaw[],
  basePath: string = "",
): RouteRecordRaw[] => {
  const result: RouteRecordRaw[] = [];
  // 遍历路由表
  routes.forEach((item) => {
    // 不存在 children && 不存在 meta 直接 return
    if (isNull(item.meta) && isNull(item.children)) return;
    // 存在 children 不存在 meta，进入迭代
    if (isNull(item.meta) && !isNull(item.children)) {
      // @ts-ignore
      result.push(...generateMenus(item.children));
      return;
    }
    // 合并 path 作为跳转路径
    const routePath = path.resolve(basePath, item.path);
    // 路由分离之后，存在同名父路由的情况，需要单独处理
    let route: RouteRecordRaw | undefined = result.find(
      (item) => item.path === routePath,
    );
    if (!route) {
      route = {
        ...item,
        path: routePath,
        children: [] as RouteRecordRaw[],
      };

      // icon 与 title 必须全部存在
      if (route.meta?.title && !route?.meta.hidden) {
        // meta 存在生成 route 对象，放入 arr
        result.push(route);
      }
    }
    // 存在 children 进入迭代到children
    if (item.children) {
      // @ts-ignore
      route.children.push(...generateMenus(item.children, route.path));
    }
  });
  return result;
};

/***
 * 获取modules目录下所有路由
 */
export const getRoutes = (): RouteRecordRaw[] => {
  const routes: RouteRecordRaw[] = [];
  const modules = import.meta.glob("@/router/modules/*.ts", { eager: true });
  for (const key in modules) {
    // @ts-ignore
    routes.push(...modules[key].default);
  }
  return routes;
};
