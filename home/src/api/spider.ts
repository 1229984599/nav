import axios from "axios";

export async function getYiyan() {
  const resp = await axios.get("https://v1.hitokoto.cn/");
  return resp.data;
}
