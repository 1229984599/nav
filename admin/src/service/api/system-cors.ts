import { request } from '../request';

/** Paginated CORS origin list */
export function fetchCorsList(
  params: { page: number; size: number },
  data: Api.CorsOrigin.CorsFilter = {},
  orderBy = 'order'
) {
  return request<Api.CorsOrigin.PageResult>({
    url: '/cors/list',
    method: 'post',
    params: { ...params, order_by: orderBy },
    data
  });
}

/** Create a CORS origin */
export function fetchCorsCreate(data: Api.CorsOrigin.CorsCreate) {
  return request({ url: '/cors/create', method: 'post', data });
}

/** Update a CORS origin */
export function fetchCorsUpdate(id: number, data: Partial<Api.CorsOrigin.CorsCreate>) {
  return request({ url: `/cors/${id}`, method: 'put', data });
}

/** Delete CORS origins by ids */
export function fetchCorsDelete(ids: string) {
  return request({ url: `/cors/${ids}`, method: 'delete' });
}

/** Batch update CORS origins (for drag sort) */
export function fetchCorsBatchUpdate(data: Array<{ id: number; order: number }>) {
  return request({ url: '/cors/update/all', method: 'put', data });
}
