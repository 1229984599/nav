import { defineStore } from "pinia";
import { RouteMeta } from "vue-router";

export interface tagsViewType {
  path: string;
  meta: RouteMeta;
}

export const useTagsViewStore = defineStore("tagsView", {
  state: () => {
    return {
      tagsViewList: [] as tagsViewType[],
    };
  },
  actions: {
    addTagsView(route: tagsViewType) {
      const tagsView = this.tagsViewList.find(
        (item) => item.path === route.path,
      );
      if (!tagsView) {
        this.tagsViewList.push(route);
      }
    },
    deleteTagsView(route: tagsViewType) {
      const tagsViewIndex = this.tagsViewList.findIndex(
        (item) => item.path === route.path,
      );
      if (tagsViewIndex !== -1) {
        this.tagsViewList.splice(tagsViewIndex, 1);
      }
    },
    closeRightTags(index: number) {
      // 删除index后所有元素
      this.tagsViewList.splice(index + 1);
    },
    closeOtherTags(index: number) {
      this.tagsViewList = [this.tagsViewList[index]];
    },
  },
  persist: {
    paths: ["tagsViewList"],
  },
});
