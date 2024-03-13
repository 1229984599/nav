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
  const data = await getDataList(`https://www.baidu.com/su?wd=${query}`, {
    jsonpCallback: "cb",
    jsonpCallbackFunction: "",
  });
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
 * 获取掘金榜单
 */
export async function getHotBySpider(name: string): Promise<any> {
  return await request({
    url: "/spider/hot",
    method: "post",
    params: {
      name: name,
    },
  });
}
