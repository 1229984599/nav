import axios from "axios";
import { request } from "@/utils/request";

export async function getYiyan() {
  const resp = await axios.get("https://v1.hitokoto.cn/");
  return resp.data;
}

/*
 */
export async function getBaiduSuggestions(query: string) {
  const response = await request({
    method: "get",
    url: `/spider/baidu`,
    params: {
      query: query,
    },
  });
  // 提取JSON部分
  // @ts-ignore
  const apiResponse = response.match(/^\(([^)]+)\)/)[1];
  const data = JSON.parse(apiResponse.replace(/(\w+)(?=:)/g, '"$1"'));
  return data.s.map((item: any) => ({
    title: item,
    menus: [{ title: "百度" }],
  }));
}
