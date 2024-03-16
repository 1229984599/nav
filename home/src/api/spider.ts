import fetchJsonp from "fetch-jsonp";
import { ElMessage } from "element-plus";
import { request } from "@/utils/request";

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
    menus: [{ title: "百度一下", icon: "https://www.baidu.com/favicon.ico" }],
  }));
}

export interface HotItemType {
  hot: string;
  title: string;
  updatetime: string;
  url: string;
}

/**
 *  获取每日榜单（通过故梦api）
 * @param name
 */
export async function getHotList(name: string = "BaiduHot"): Promise<any> {
  if (["JueJinHot", "52PoJieHot"].includes(name)) {
    return await getHotBySpider(name);
  }
  const res = await getDataList(
    `https://api.gumengya.com/Api/${name}?format=jsonp`,
  );
  if (res.code === 200) {
    return res.data;
  }
  ElMessage.error(`${name}\t获取热搜失败`);
}

/**
 * 获取每日一言
 */
export async function getYiyan(): Promise<string> {
  const { text } = await getHotList("YiYan");
  return text;
}

/**
 * 获取服务器榜单：（掘金、52pojie）
 */
export async function getHotBySpider(name: string): Promise<any> {
  return await request({
    url: "/spider/hot",
    method: "get",
    params: {
      name,
    },
  });
}

export interface WeatherType {
  obsTime?: string;
  temp?: string;
  feelsLike?: string;
  icon?: string;
  text?: string;
  wind360?: string;
  windDir?: string;
  windScale?: string;
  windSpeed?: string;
  humidity?: string;
  precip?: string;
  pressure?: string;
  vis?: string;
  cloud?: string;
  dew?: string;
}

export interface FutureWeatherType {
  fxDate?: string;
  sunrise?: string;
  sunset?: string;
  moonrise?: string;
  moonset?: string;
  moonPhase?: string;
  moonPhaseIcon?: string;
  tempMax?: string;
  tempMin?: string;
  iconDay?: string;
  textDay?: string;
  iconNight?: string;
  textNight?: string;
  wind360Day?: string;
  windDirDay?: string;
  windScaleDay?: string;
  windSpeedDay?: string;
  wind360Night?: string;
  windDirNight?: string;
  windScaleNight?: string;
  windSpeedNight?: string;
  humidity?: string;
  precip?: string;
  pressure?: string;
  vis?: string;
  cloud?: string;
  uvIndex?: string;
}

export interface WeatherRespType {
  city: string;
  weather: WeatherType;
  future_weather: FutureWeatherType[];
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
