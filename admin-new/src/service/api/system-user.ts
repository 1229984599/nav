import { request } from '../request';

/** Paginated user list */
export function fetchUserList(params: { page: number; size: number }, data: Api.SystemUser.UserFilter = {}) {
  return request<Api.SystemUser.PageResult>({
    url: '/system/user/list',
    method: 'post',
    params,
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

/** Delete users by ids */
export function fetchUserDelete(ids: string) {
  return request({ url: `/system/user/${ids}`, method: 'delete' });
}
