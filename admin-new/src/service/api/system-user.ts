import { request } from '../request';

/** Paginated user list */
export function fetchUserList(params: { page: number; size: number }, data: Api.SystemUser.UserFilter = {}, orderBy = '-create_time') {
  return request<Api.SystemUser.PageResult>({
    url: '/system/user/list',
    method: 'post',
    params: { ...params, order_by: orderBy },
    data
  });
}

/** Create a user */
export function fetchUserCreate(data: Api.SystemUser.UserCreate) {
  return request({ url: '/system/user/create', method: 'post', data });
}

/** Update a user */
export function fetchUserUpdate(id: number, data: Api.SystemUser.UserUpdate) {
  return request({ url: `/system/user/${id}`, method: 'put', data });
}

/** Batch update users (for drag sort) */
export function fetchUserBatchUpdate(data: Array<{ id: number; order: number }>) {
  return request({ url: '/system/user/update/all', method: 'put', data });
}

/** Delete users by ids */
export function fetchUserDelete(ids: string) {
  return request({ url: `/system/user/${ids}`, method: 'delete' });
}
