import { defineStore } from "pinia";
import { FriendSchemaList } from "@/api/friend/types";
import friendModel from "@/api/friend";

/**
 * 记录分友情链接
 */
export const useFriendStore = defineStore("friend", {
  state: () => ({
    friendList: new Array<FriendSchemaList>(),
  }),
  actions: {
    async getFriendList() {
      const { items } = await friendModel.list({ page: 1, pageSize: 100 });
      this.friendList = items;
      return items;
    },
  },
  persist: true,
});
