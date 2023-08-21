import axios from "axios";

export async function getYiyan() {
  const resp = await axios.get("https://v1.hitokoto.cn/");
  return resp.data;
}

export async function getBaiduSuggestions(query: string) {
  const response = await axios.get(
    `https://www.baidu.com/su?wd=${encodeURIComponent(query)}&cb=`,
  );
  // 提取JSON部分
  const apiResponse = response.data.match(/^\(([^)]+)\)/)[1];
  const data = JSON.parse(apiResponse.replace(/(\w+)(?=:)/g, '"$1"'));
  return data.s;
}
