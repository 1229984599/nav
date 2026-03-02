/** 本地书签链接（扩展自 LinkSchemaList，增加 id、使用追踪和分组） */
export interface LocalLink {
  id: string;
  href: string;
  title: string;
  icon: string;
  color: string;
  desc: string;
  is_self: boolean;
  clickCount: number;
  lastClickedAt: number;
  createdAt: number;
  groupIds: string[];
}

/** 书签分组 */
export interface BookmarkGroup {
  id: string;
  name: string;
  icon: string;
  color: string;
  order: number;
}

/** 书签视图模式 */
export type BookmarkViewMode = "grid" | "compact" | "list";

/** 书签排序模式 */
export type BookmarkSortMode = "manual" | "frequency" | "recent" | "alpha";

/** 书签 Store 完整状态 */
export interface LocalBookmarksState {
  groups: BookmarkGroup[];
  links: LocalLink[];
  viewMode: BookmarkViewMode;
  sortMode: BookmarkSortMode;
  activeGroupId: string | null;
}

/** 导入/导出 JSON 格式 */
export interface BookmarkExportData {
  version: 1;
  exportedAt: string;
  groups: BookmarkGroup[];
  links: LocalLink[];
}

/** 默认分组 ID */
export const DEFAULT_GROUP_ID = "__default__";

/** 默认分组 */
export const DEFAULT_GROUP: BookmarkGroup = {
  id: DEFAULT_GROUP_ID,
  name: "未分类",
  icon: "ion:bookmarks",
  color: "#C71585",
  order: 0,
};
