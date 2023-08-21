import { RouteRecordRaw } from "vue-router";
import { getRoutes } from "@/utils/route";

/**
 * 私有路由表
 * 自动获取module下的路由文件，并生成路由表
 */
export const privateRoutes: RouteRecordRaw[] = getRoutes();
