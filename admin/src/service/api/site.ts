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

/** Create a full site backup */
export function fetchSiteBackup() {
  return request<{ filename: string; path: string }>({ url: '/site/backup', method: 'post' });
}

/** List all backup files */
export function fetchSiteBackupList() {
  return request<Array<{ filename: string; size: number; created_at: string }>>({ url: '/site/backup/list' });
}

/** Delete a backup file */
export function fetchSiteBackupDelete(filename: string) {
  return request({ url: `/site/backup/${filename}`, method: 'delete' });
}

/** Restore from a backup file on server */
export function fetchSiteRestore(filename: string) {
  return request({ url: '/site/restore', method: 'post', params: { filename } });
}

/** Restore from an uploaded backup file */
export function fetchSiteRestoreUpload(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return request({
    url: '/site/restore',
    method: 'post',
    headers: { 'Content-Type': 'multipart/form-data' },
    data: formData
  });
}
