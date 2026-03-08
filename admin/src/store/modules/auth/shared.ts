import { localStg } from '@/utils/storage';

/** Get token — tries admin storage first, falls back to home's localStorage */
export function getToken() {
  const adminToken = localStg.get('token');
  if (adminToken) return adminToken;

  // Fallback: read from home app's pinia-persisted "user" key
  try {
    const raw = localStorage.getItem('user');
    if (raw) {
      const homeData = JSON.parse(raw);
      const accessToken = homeData?.token?.access_token;
      if (accessToken) {
        // Promote to admin format so subsequent requests use it directly
        localStg.set('token', accessToken);
        if (homeData.token.refresh_token) {
          localStg.set('refreshToken', homeData.token.refresh_token);
        }
        return accessToken;
      }
    }
  } catch {
    // ignore parse errors
  }

  return '';
}

/** Clear auth storage for both admin and home */
export function clearAuthStorage() {
  localStg.remove('token');
  localStg.remove('refreshToken');
  // Also clear home's storage so both apps log out together
  localStorage.removeItem('user');
}

/** Sync token to home app's localStorage format after admin login */
export function syncTokenToHome(loginToken: Api.Auth.LoginToken) {
  try {
    const homeData: Record<string, any> = {};
    homeData.token = {
      access_token: loginToken.token,
      refresh_token: loginToken.refreshToken,
      expires: loginToken.expires || new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    };
    localStorage.setItem('user', JSON.stringify(homeData));
  } catch {
    // ignore
  }
}

/** Sync user info to home app's localStorage format */
export function syncUserInfoToHome(userInfo: Api.Auth.UserInfo) {
  try {
    const raw = localStorage.getItem('user');
    const homeData = raw ? JSON.parse(raw) : {};
    homeData.userInfo = {
      id: Number(userInfo.userId),
      username: userInfo.userName,
      nickname: userInfo.nickName || userInfo.userName
    };
    // Also mark session as verified
    homeData.sessionVerified = true;
    localStorage.setItem('user', JSON.stringify(homeData));
  } catch {
    // ignore
  }
}
