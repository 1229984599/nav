import axios, { type AxiosInstance, type AxiosRequestConfig } from "axios";
import { ElMessage } from "element-plus";
// @ts-ignore
import { get, merge } from "lodash-es";
import { useUserStore } from "@/store/user";

/** 扩展 AxiosRequestConfig 支持静默模式 */
export interface RequestConfig extends AxiosRequestConfig {
  /** 静默模式：不显示错误提示 */
  silent?: boolean;
}

/** 创建请求实例 */
function createService() {
  // 创建一个 axios 实例命名为 service
  const service = axios.create();
  // 请求拦截
  service.interceptors.request.use(
    (config) => config,
    // 发送失败
    (error) => Promise.reject(error),
  );
  // 响应拦截（可根据具体业务作出相应的调整）
  service.interceptors.response.use(
    (response) => {
      // apiData 是 api 返回的数据
      const apiData = response.data;
      // 二进制数据则直接返回
      const responseType = response.request?.responseType;
      if (responseType === "blob" || responseType === "arraybuffer")
        return apiData;
      // 这个 code 是和后端约定的业务 code
      const code = apiData.code;
      // 如果没有 code, 代表这不是项目后端开发的 api
      if (code === undefined) {
        if (!(response.config as RequestConfig)?.silent) {
          ElMessage.error("非本系统的接口");
        }
        return Promise.reject(new Error("非本系统的接口"));
      }
      switch (code) {
        case 200:
          // 本系统采用 code === 200 来表示没有业务错误
          return apiData.data;

        default:
          // 不是正确的 code
          if (!(response.config as RequestConfig)?.silent) {
            ElMessage.error(apiData.message || "Error");
          }
          return Promise.reject(new Error("Error"));
      }
    },
    (error) => {
      if (!error.config?.silent) {
        ElMessage.error(error.message || "请求失败");
      }
      return Promise.reject(error);
    },
  );
  return service;
}

/** 创建请求方法 */
function createRequest(service: AxiosInstance) {
  return function <T>(config: RequestConfig): Promise<T> {
    const userStore = useUserStore();
    const hasToken = !!userStore.token?.access_token;

    // 仅在有 token 时检查过期
    if (hasToken && userStore.token?.expires && new Date(userStore.token.expires) < new Date()) {
      userStore.logout();
      ElMessage.warning("登录已过期，请重新登录");
      return Promise.reject(new Error("登录已过期，请重新登录"));
    }

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    // 仅在有有效 token 时携带 Authorization
    if (hasToken) {
      headers.Authorization = `Bearer ${userStore.token.access_token}`;
    }

    const defaultConfig = {
      headers,
      timeout: 15000,
      baseURL: import.meta.env.VITE_BASE_API || "/api",
      data: {},
    };
    // 将默认配置 defaultConfig 和传入的自定义配置 config 进行合并成为 mergeConfig
    const mergeConfig = merge(defaultConfig, config);
    return service(mergeConfig);
  };
}

/** 用于网络请求的实例 */
const service = createService();
/** 用于网络请求的方法 */
export const request = createRequest(service);
