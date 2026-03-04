import fetchJsonp from "fetch-jsonp";
import { ElMessage } from "element-plus";
import { request } from "@/utils/request";
import { WeatherRespType, HotListResponse } from "@/api/spider/types";
import { sample } from "lodash-es";

// 通过fetchJsonp库来实现跨域请求
function getDataList(
  url: string,
  options: fetchJsonp.Options = {},
): Promise<any> {
  return new Promise((resolve, reject) => {
    fetchJsonp(url, {
      ...options,
    })
      .then((response) => {
        if (response.ok) {
          return resolve(response.json());
        }
        ElMessage.error("网络错误");
        return reject(new Error("网络错误"));
      })
      .catch((error) => {
        return reject(error);
      });
  });
}

/**
 *  获取百度搜索建议
 * @param query
 */
export async function getBaiduSuggestions(query: string) {
  const encodedKeyword = encodeURIComponent(query);
  const data = await getDataList(
    `https://www.baidu.com/su?wd=${encodedKeyword}`,
    {
      jsonpCallback: "cb",
      jsonpCallbackFunction: "",
    },
  );
  return data.s.map((item: any) => ({
    title: item,
    menus: [
      {
        title: "百度一下",
        icon: "ant-design:baidu-outlined",
        color: "#7f7eed",
      },
    ],
  }));
}

/**
 *  获取每日榜单（通过后端pearktrue API）
 * @param name 平台中文名，如 百度、哔哩哔哩、微博
 */
export async function getHotList(name: string = "百度"): Promise<HotListResponse | null> {
  return await request({
    url: "/spider/hot",
    method: "get",
    params: { name },
  });
}

/**
 * 获取每日一言（通过后端 hitokoto）
 */
export async function getYiyan(): Promise<string> {
  const res: any = await request({
    url: "/spider/yiyan",
    method: "get",
  });
  return res?.hitokoto || '';
}

/**
 * 获取和风天气数据
 * @param location
 */
export async function getWeather(location: string): Promise<WeatherRespType> {
  return await request({
    url: "/spider/weather",
    method: "get",
    params: {
      location,
    },
  });
}

/**
 * 获取每日随机背景图片
 */
const name_list = [
  "FjImg",
  "DmImgS",
  "DmImg",
  "MvImg",
  "QcImg",
  "McImg",
  "BingImg",
];

export async function getRandImg(name: string = "") {
  const randName = name || sample(name_list);
  const res = await getDataList(
    `https://api.gumengya.com/Api/${randName}?format=jsonp`,
  );
  if (res.code === 200) {
    return res.data.url;
  }
}
