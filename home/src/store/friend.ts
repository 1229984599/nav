import { defineStore } from "pinia";
import { FriendSchemaList } from "@/api/friend/types";
import friendModel from "@/api/friend";

/**
 * 记录分类和所有数据
 */
export const useFriendStore = defineStore("friend", {
  state: () => ({
    friendList: new Array<FriendSchemaList>(),
  }),
  actions: {
    async getFriendList() {
      const { items } = await friendModel.list(1, 100);
      this.friendList = items;
      return items;
    },
  },
});
