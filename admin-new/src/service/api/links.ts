import { request } from '../request';

/** Paginated link list */
export function fetchLinkList(
  params: { page: number; size: number },
  data: Api.Links.LinkFilter = {},
  orderBy = '-create_time'
) {
  return request<Api.Links.PageResult>({
    url: '/links/list',
    method: 'post',
    params: { ...params, order_by: orderBy },
    data
  });
}

/** Read a single link */
export function fetchLinkRead(id: number) {
  return request<Api.Links.LinkItem>({ url: `/links/read/${id}` });
}

/** Create a link */
export function fetchLinkCreate(data: Api.Links.LinkCreate) {
  return request({ url: '/links/create', method: 'post', data });
}

/** Update a link */
export function fetchLinkUpdate(id: number, data: Api.Links.LinkCreate) {
  return request({ url: `/links/${id}`, method: 'put', data });
}

/** Delete links by ids (comma-separated) */
export function fetchLinkDelete(ids: string) {
  return request({ url: `/links/${ids}`, method: 'delete' });
}

/** Spider site info from URL */
export function fetchLinkSiteInfo(url: string) {
  return request<Api.Links.SiteInfo>({ url: '/links/siteinfo', method: 'post', params: { url } });
}

/** Sync icon to CDN by URL */
export function fetchLinkSyncCdn(url: string, linkId?: number) {
  return request({ url: '/links/sync_cdn', method: 'post', params: { url, link_id: linkId } });
}

/** Sync uploaded file to CDN */
export function fetchLinkSyncCdnFile(file: File, linkId?: number) {
  const formData = new FormData();
  formData.append('file', file);
  return request({
    url: '/links/sync_cdn_file',
    method: 'post',
    params: { link_id: linkId },
    headers: { 'Content-Type': 'multipart/form-data' },
    data: formData
  });
}
