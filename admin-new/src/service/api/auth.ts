import { request } from '../request';

/**
 * Login
 *
 * @param userName User name
 * @param password Password
 */
export function fetchLogin(userName: string, password: string) {
  return request<Api.Auth.LoginToken>({
    url: '/system/login/login',
    method: 'post',
    data: {
      username: userName,
      password
    }
  });
}

/** Get user info */
export function fetchGetUserInfo() {
  return request<Api.Auth.UserInfo>({ url: '/system/login/getUserInfo' });
}

/**
 * Refresh token
 *
 * @param refreshToken Refresh token
 */
export function fetchRefreshToken(refreshToken: string) {
  return request<Api.Auth.LoginToken>({
    url: '/system/login/refreshToken',
    method: 'post',
    headers: {
      Authorization: `Bearer ${refreshToken}`
    }
  });
}

/** Update current user profile */
export function fetchUpdateProfile(data: { nickname: string }) {
  return request({ url: '/system/login/updateProfile', method: 'put', data });
}

/** Change current user password */
export function fetchChangePassword(data: { old_password: string; new_password: string }) {
  return request({ url: '/system/login/changePassword', method: 'put', data });
}
