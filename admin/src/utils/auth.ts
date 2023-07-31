import Cookies from "js-cookie";
import { storageSession } from "@pureadmin/utils";
import { useUserStoreHook } from "@/store/modules/user";
import { Token, UserRead,UserSchemaRead } from "@/api/login/types";


export const sessionKey = "user-info";
export const TokenKey = "authorized-token";

/** 获取`token` */
export function getToken(): Token {
  // 此处与`TokenKey`相同，此写法解决初始化时`Cookies`中不存在`TokenKey`报错
  return Cookies.get(TokenKey)
    ? JSON.parse(Cookies.get(TokenKey))
    : storageSession().getItem(TokenKey);
}

function setSessionKey(username: string, roles: Array<string>) {
  useUserStoreHook().SET_USERNAME(username);
  useUserStoreHook().SET_ROLES(roles);
  storageSession().setItem(sessionKey, {
    username,
    roles
  });
}

export function setUserInfo(user: UserRead) {
  if (user.username && user.roles) {
    let { username, roles } = user;
    setSessionKey(username, roles.map(item => item.name));
  } else {
    const username =
      storageSession().getItem<UserSchemaRead>(sessionKey)?.username ?? "";
    const roles =
      storageSession().getItem<UserSchemaRead>(sessionKey)?.roles ?? [];
    setSessionKey(username, roles);
  }
}

/**
 * @description 设置`token`以及一些必要信息并采用无感刷新`token`方案
 * 无感刷新：后端返回`accessToken`（访问接口使用的`token`）、`refreshToken`（用于调用刷新`accessToken`的接口时所需的`token`，`refreshToken`的过期时间（比如30天）应大于`accessToken`的过期时间（比如2小时））、`expires`（`accessToken`的过期时间）
 * 将`accessToken`、`expires`这两条信息放在key值为authorized-token的cookie里（过期自动销毁）
 * 将`username`、`roles`、`refreshToken`、`expires`这四条信息放在key值为`user-info`的sessionStorage里（浏览器关闭自动销毁）
 */
export function setToken(token: Token) {
  let expires = 0;
  const { access_token, refresh_token } = token;
  expires = new Date(token.expires).getTime(); // 如果后端直接设置时间戳，将此处代码改为expires = data.expires，然后把上面的DataInfo<Date>改成DataInfo<number>即可
  const cookieString = JSON.stringify({ access_token, expires });

  expires > 0
    ? Cookies.set(TokenKey, cookieString, {
        expires: (expires - Date.now()) / 86400000
      })
    : Cookies.set(TokenKey, cookieString);
  storageSession().setItem(TokenKey, {
    access_token,
    refresh_token,
    expires
  });
}

/** 删除`token`以及key值为`user-info`的session信息 */
export function removeToken() {
  Cookies.remove(TokenKey);
  sessionStorage.clear();
}

/** 格式化token（jwt格式） */
export const formatToken = (token: string): string => {
  return "Bearer " + token;
};
