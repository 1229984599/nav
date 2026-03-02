import { defineStore } from "pinia";
import type {
  LocalLink,
  BookmarkGroup,
  BookmarkViewMode,
  BookmarkSortMode,
  LocalBookmarksState,
  BookmarkExportData,
} from "@/types/bookmark";
import { DEFAULT_GROUP_ID, DEFAULT_GROUP } from "@/types/bookmark";

/** 按排序模式排序链接 */
function sortLinks(links: LocalLink[], mode: BookmarkSortMode): LocalLink[] {
  const arr = [...links];
  switch (mode) {
    case "frequency":
      return arr.sort((a, b) => b.clickCount - a.clickCount);
    case "recent":
      return arr.sort((a, b) => b.lastClickedAt - a.lastClickedAt);
    case "alpha":
      return arr.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
    case "manual":
    default:
      return arr;
  }
}

/** 兼容旧数据：将 groupId 迁移为 groupIds */
function normalizeLink(link: any): LocalLink {
  if (link.groupIds && Array.isArray(link.groupIds)) return link;
  const groupId = link.groupId || DEFAULT_GROUP_ID;
  const { groupId: _, ...rest } = link;
  return { ...rest, groupIds: [groupId] };
}

export const useBookmarkStore = defineStore("bookmark", {
  state: (): LocalBookmarksState => ({
    groups: [{ ...DEFAULT_GROUP }],
    links: [],
    viewMode: "grid",
    sortMode: "manual",
    activeGroupId: null,
  }),

  getters: {
    /** 按 order 排序的分组列表 */
    sortedGroups: (state): BookmarkGroup[] => {
      return [...state.groups].sort((a, b) => a.order - b.order);
    },

    /** 当前激活分组（或全部）的链接，按排序模式排序 */
    activeLinks: (state): LocalLink[] => {
      const filtered = state.activeGroupId
        ? state.links.filter((l) => l.groupIds.includes(state.activeGroupId!))
        : state.links;
      return sortLinks(filtered, state.sortMode);
    },

    /** 总书签数 */
    totalCount: (state): number => state.links.length,

    /** 各分组书签计数（一个链接属于多个分组时各分组都计数） */
    groupCounts: (state): Record<string, number> => {
      const counts: Record<string, number> = {};
      for (const g of state.groups) counts[g.id] = 0;
      for (const l of state.links) {
        for (const gid of l.groupIds) {
          counts[gid] = (counts[gid] || 0) + 1;
        }
      }
      return counts;
    },
  },

  actions: {
    // ---- 数据初始化钩子：兼容 groupId → groupIds ----

    $hydrate() {
      this.links = this.links.map(normalizeLink);
    },

    // ---- Link CRUD ----

    addLink(
      link: Omit<LocalLink, "id" | "clickCount" | "lastClickedAt" | "createdAt">
    ) {
      const newLink: LocalLink = {
        ...link,
        id: crypto.randomUUID(),
        clickCount: 0,
        lastClickedAt: 0,
        createdAt: Date.now(),
        groupIds:
          link.groupIds && link.groupIds.length > 0
            ? link.groupIds
            : [DEFAULT_GROUP_ID],
      };
      this.links.push(newLink);
    },

    updateLink(id: string, updates: Partial<LocalLink>) {
      const idx = this.links.findIndex((l) => l.id === id);
      if (idx !== -1) {
        this.links[idx] = { ...this.links[idx], ...updates };
      }
    },

    deleteLink(id: string) {
      this.links = this.links.filter((l) => l.id !== id);
    },

    recordClick(id: string) {
      const link = this.links.find((l) => l.id === id);
      if (link) {
        link.clickCount++;
        link.lastClickedAt = Date.now();
      }
    },

    /** 切换链接在某个分组中的归属（添加或移除） */
    toggleLinkGroup(linkId: string, groupId: string) {
      const link = this.links.find((l) => l.id === linkId);
      if (!link) return;
      const idx = link.groupIds.indexOf(groupId);
      if (idx >= 0) {
        // 移除，但至少保留一个分组
        if (link.groupIds.length > 1) {
          link.groupIds.splice(idx, 1);
        }
      } else {
        link.groupIds.push(groupId);
      }
    },

    /** 设置链接的分组（替换全部） */
    setLinkGroups(linkId: string, groupIds: string[]) {
      const link = this.links.find((l) => l.id === linkId);
      if (!link) return;
      link.groupIds = groupIds.length > 0 ? groupIds : [DEFAULT_GROUP_ID];
    },

    // ---- Group CRUD ----

    addGroup(group: Omit<BookmarkGroup, "id" | "order">) {
      const newGroup: BookmarkGroup = {
        ...group,
        id: crypto.randomUUID(),
        order: this.groups.length,
      };
      this.groups.push(newGroup);
      return newGroup.id;
    },

    updateGroup(id: string, updates: Partial<BookmarkGroup>) {
      const idx = this.groups.findIndex((g) => g.id === id);
      if (idx !== -1) {
        this.groups[idx] = { ...this.groups[idx], ...updates };
      }
    },

    deleteGroup(id: string) {
      if (id === DEFAULT_GROUP_ID) return;
      // 删除分组时，从所有链接的 groupIds 中移除该分组
      this.links.forEach((l) => {
        const idx = l.groupIds.indexOf(id);
        if (idx >= 0) {
          l.groupIds.splice(idx, 1);
          // 确保至少属于一个分组
          if (l.groupIds.length === 0) {
            l.groupIds.push(DEFAULT_GROUP_ID);
          }
        }
      });
      this.groups = this.groups.filter((g) => g.id !== id);
      if (this.activeGroupId === id) this.activeGroupId = null;
    },

    reorderGroups(orderedIds: string[]) {
      orderedIds.forEach((id, index) => {
        const g = this.groups.find((g) => g.id === id);
        if (g) g.order = index;
      });
    },

    // ---- View / Sort ----

    setViewMode(mode: BookmarkViewMode) {
      this.viewMode = mode;
    },
    setSortMode(mode: BookmarkSortMode) {
      this.sortMode = mode;
    },
    setActiveGroup(groupId: string | null) {
      this.activeGroupId = groupId;
    },

    // ---- Import / Export ----

    exportData(): BookmarkExportData {
      return {
        version: 1,
        exportedAt: new Date().toISOString(),
        groups: this.groups,
        links: this.links,
      };
    },

    importData(data: BookmarkExportData, mode: "replace" | "merge" = "replace") {
      // 兼容旧格式数据
      const normalizedLinks = data.links.map(normalizeLink);
      if (mode === "replace") {
        this.groups = data.groups;
        this.links = normalizedLinks;
      } else {
        const existingGroupIds = new Set(this.groups.map((g) => g.id));
        const existingHrefs = new Set(this.links.map((l) => l.href));
        for (const g of data.groups) {
          if (!existingGroupIds.has(g.id)) this.groups.push(g);
        }
        for (const l of normalizedLinks) {
          if (!existingHrefs.has(l.href)) {
            this.links.push({ ...l, id: crypto.randomUUID() });
          }
        }
      }
      // 确保默认分组存在
      if (!this.groups.find((g) => g.id === DEFAULT_GROUP_ID)) {
        this.groups.unshift({ ...DEFAULT_GROUP });
      }
    },

    // ---- 从旧格式迁移 ----

    migrateFromLegacy(oldLinks: any[]) {
      if (this.links.length > 0) return; // 已有数据，跳过迁移
      for (const old of oldLinks) {
        this.addLink({
          href: old.href || "",
          title: old.title || "",
          icon: old.icon || "",
          color: old.color || "",
          desc: old.desc || "",
          is_self: old.is_self || false,
          groupIds: [DEFAULT_GROUP_ID],
        });
      }
    },

    // ---- Reset ----

    resetAll() {
      this.groups = [{ ...DEFAULT_GROUP }];
      this.links = [];
      this.activeGroupId = null;
    },
  },

  persist: {
    paths: ["groups", "links", "viewMode", "sortMode", "activeGroupId"],
    afterRestore(ctx) {
      // 持久化恢复后兼容旧数据
      ctx.store.links = ctx.store.links.map(normalizeLink);
    },
  },
});
