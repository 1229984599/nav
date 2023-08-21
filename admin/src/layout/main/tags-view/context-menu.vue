<script lang="ts">
export default {
  name: "MContextMenu",
};
</script>
<script setup lang="ts">
import { useRouter } from "vue-router";
import { useTagsViewStore } from "@/store";
import { onClickOutside, useVModel } from "@vueuse/core";
import { ref } from "vue";

const props = defineProps({
  index: {
    type: Number,
    required: true,
  },
  isVisible: {
    type: Boolean,
    required: true,
  },
});
const isVisible = useVModel(props, "isVisible");
const router = useRouter();
const tagsViewStore = useTagsViewStore();

function handleRefresh() {
  router.go(0);
}

function handleOther() {
  router.push(tagsViewStore.tagsViewList[props.index].path);
  tagsViewStore.closeOtherTags(<number>props.index);
  isVisible.value = false;
}

function handleRight() {
  router.push(tagsViewStore.tagsViewList[props.index].path);
  tagsViewStore.closeRightTags(<number>props.index);
  isVisible.value = false;
}

// 点击区域外也要关闭
const target = ref(null);
onClickOutside(target, () => (isVisible.value = false));
</script>

<template>
  <ul
    ref="target"
    class="fixed flex flex-col p-1 text-zinc-700 bg-white cursor-pointer text-sm rounded z-40 shadow-2xl shadow-gray-900/3"
  >
    <li @click="handleRefresh">刷新</li>
    <li @click="handleRight">关闭右侧</li>
    <li @click="handleOther">关闭其他</li>
  </ul>
</template>

<style lang="scss" scoped>
li {
  @apply px-4 py-1 hover:bg-gray-100;
}
</style>
