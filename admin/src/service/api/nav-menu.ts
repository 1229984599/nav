import { request } from '../request';

/** Paginated menu list */
export function fetchMenuList(params: { page: number; size: number }, data: Api.NavMenu.MenuFilter = {}) {
  return request<Api.NavMenu.PageResult>({
    url: '/menu/list',
    method: 'post',
    params,
    data
  });
}

/** Get menu tree */
export function fetchMenuTree() {
  return request<Api.NavMenu.MenuTreeNode[]>({ url: '/menu/tree' });
}

/** Create a menu */
export function fetchMenuCreate(data: Api.NavMenu.MenuCreate) {
  return request({ url: '/menu/create', method: 'post', data });
}

/** Update a menu */
export function fetchMenuUpdate(id: number, data: Api.NavMenu.MenuCreate) {
  return request({ url: `/menu/${id}`, method: 'put', data });
}

/** Batch update menus (for drag sort) */
export function fetchMenuBatchUpdate(data: Array<{ id: number; order: number }>) {
  return request({ url: '/menu/update/all', method: 'put', data });
}

/** Delete menus by ids */
export function fetchMenuDelete(ids: string) {
  return request({ url: `/menu/${ids}`, method: 'delete' });
}

/** Import menus from JSON file */
export function fetchMenuImport(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return request<{ created: number; skipped: number }>({
    url: '/menu/import',
    method: 'post',
    headers: { 'Content-Type': 'multipart/form-data' },
    data: formData
  });
}
