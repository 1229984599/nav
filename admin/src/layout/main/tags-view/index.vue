<script lang="ts">
export default {
  name: "MTagsView",
};
</script>
<script setup lang="ts">
import MTagItem from "./tag-item.vue";
import { useTagsViewStore } from "@/store";
import MContextMenu from "./context-menu.vue";
import { reactive, ref } from "vue";

const tagsViewStore = useTagsViewStore();
const menuStyle = reactive({
  left: "0",
  top: "0",
});
// 记录当前tag索引
const itemIndex = ref(0);
// tags是否可见
const isVisible = ref(false);

function handleContextMenu($event: PointerEvent, index: number) {
  isVisible.value = true;
  const { x, y } = $event;
  menuStyle.left = `${x}px`;
  menuStyle.top = `${y}px`;
  itemIndex.value = index;
}
</script>

<template>
  <div class="tags-view-container">
    <el-scrollbar>
      <div class="flex">
        <m-tag-item
          class="shrink-0"
          @contextmenu.prevent="handleContextMenu($event, index)"
          :item="tagItem"
          v-for="(tagItem, index) in tagsViewStore.tagsViewList"
        />
      </div>
    </el-scrollbar>

    <m-context-menu
      v-model:is-visible="isVisible"
      v-show="isVisible"
      :index="itemIndex"
      :style="menuStyle"
    />
  </div>
</template>

<style lang="scss" scoped>
.tags-view-container {
  margin-top: 4px;
  height: 38px;
  width: 100%;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
  box-shadow:
    0 1px 3px 0 rgba(0, 0, 0, 0.12),
    0 0 3px 0 rgba(0, 0, 0, 0.04);

  &:first-child {
    padding-left: 15px;
  }
}
</style>
