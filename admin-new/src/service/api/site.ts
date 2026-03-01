import { request } from '../request';

/** Get site settings */
export function fetchSiteGet() {
  return request<Api.Site.SiteInfo>({ url: '/site/get' });
}

/** Update site settings */
export function fetchSiteUpdate(data: Api.Site.SiteUpdate) {
  return request({ url: '/site/update', method: 'post', data });
}

/** Clear site cache */
export function fetchSiteClearCache() {
  return request({ url: '/site/clear_cache', method: 'post' });
}
