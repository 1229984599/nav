<script lang="ts">
export default {
  name: "MTagItem",
};
</script>
<script setup lang="ts">
import { computed, defineProps, PropType } from "vue";
import { tagsViewType, useTagsViewStore } from "@/store/modules/tagsview";
import { useAppStore } from "@/store";
import { useRoute } from "vue-router";
import MIcon from "@/components/icon.vue";

const appStore = useAppStore();
const tagsViewStore = useTagsViewStore();

const props = defineProps({
  item: {
    required: true,
    type: Object as PropType<tagsViewType>,
  },
});
const route = useRoute();
const isActive = computed(() => {
  return props.item?.path === route.path;
});
</script>

<template>
  <router-link
    :to="item.path"
    class="inline-flex px-3 py-2 gap-x-1 tag-item"
    :style="{ background: isActive ? appStore.cssVar.menuBg : '' }"
  >
    <span class="text-xs" :class="{ active: isActive }">{{
      item.meta?.title
    }}</span>
    <m-icon
      @click="tagsViewStore.deleteTagsView(route)"
      v-if="!isActive"
      icon="carbon:close-outline"
    />
  </router-link>
</template>

<style lang="scss" scoped>
.tag-item {
  margin-left: 5px;
  border: 1px solid #d8dce5;
  color: #495060;
  background: #fff;

  .active {
    color: #fff;

    &::before {
      content: "";
      background: #fff;
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      position: relative;
      margin-right: 4px;
    }
  }
}
</style>
