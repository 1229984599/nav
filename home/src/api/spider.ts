import { request } from "@/utils/request";

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

export interface HotItemType {
  hot: string;
  title: string;
  updatetime: string;
  url: string;
}

export async function getHotList(name: string = "BaiduHot"): Promise<any> {
  return await request({
    method: "post",
    url: "/spider/hot",
    params: {
      name,
    },
  });
}

// 不通过服务器代理转发
// export async function getHotList(
//   name: string = "BaiduHot",
//   hotParams = {},
// ): Promise<any> {
//   const { data } = await axios({
//     method: "post",
//     url: `/hotapi/${name}`,
//     params: {
//       format: "json",
//       ...hotParams,
//     },
//   });
//   if (data.code === 200) {
//     return data.data;
//   }
//   new Error("获取数据失败");
//   // debugger;
// }

export async function getYiyan(): Promise<string> {
  const { text } = await getHotList("YiYan");
  return text;
}
