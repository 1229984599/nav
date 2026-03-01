import { request } from '../request';

/** Paginated friend list */
export function fetchFriendList(
  params: { page: number; size: number },
  data: Api.Friend.FriendFilter = {},
  orderBy = '-create_time'
) {
  return request<Api.Friend.PageResult>({
    url: '/friend/list',
    method: 'post',
    params: { ...params, order_by: orderBy },
    data
  });
}

/** Read a single friend */
export function fetchFriendRead(id: number) {
  return request<Api.Friend.FriendItem>({ url: `/friend/read/${id}` });
}

/** Create a friend link */
export function fetchFriendCreate(data: Api.Friend.FriendCreate) {
  return request({ url: '/friend/create', method: 'post', data });
}

/** Update a friend link */
export function fetchFriendUpdate(id: number, data: Api.Friend.FriendCreate) {
  return request({ url: `/friend/${id}`, method: 'put', data });
}

/** Delete friends by ids */
export function fetchFriendDelete(ids: string) {
  return request({ url: `/friend/${ids}`, method: 'delete' });
}

/** Spider site info */
export function fetchFriendSiteInfo(url: string) {
  return request<Api.Links.SiteInfo>({ url: '/friend/siteinfo', method: 'post', params: { url } });
}
