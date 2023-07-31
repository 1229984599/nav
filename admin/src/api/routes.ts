import { http } from "@/utils/http";

export const getAsyncRoutes = () => {
  return http.post("routes");
};
