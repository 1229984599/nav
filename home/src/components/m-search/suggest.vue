<script setup lang="ts">
import { ref, Ref } from "vue";
import { onClickOutside, watchDebounced } from "@vueuse/core";
import { getBaiduSuggestions } from "@/api/spider";
import { useSearchStore } from "@/store/search";

defineOptions({
  name: "MSuggest",
});
const props = defineProps({
  searchQuery: {
    type: String,
    required: true,
  },
});

const searchStore = useSearchStore();
const suggestList: Ref<string[]> = ref([]);
const suggestRef = ref(null);
onClickOutside(suggestRef, () => (suggestList.value = []));
// 监听查询字段
watchDebounced(
  () => props.searchQuery,
  async () => {
    if (props.searchQuery.trim()) {
      suggestList.value = await getBaiduSuggestions(props.searchQuery);
    } else {
      suggestList.value = [];
    }
  },
  { debounce: 300, maxWait: 1000 },
);

function handleSearch(wd: string) {
  const url = `${searchStore.currentItem.url}${wd}`;
  window.open(url, "_blank");
}
</script>

<template>
  <!--    搜索推荐-->
  <div
    ref="suggestRef"
    v-show="suggestList.length > 0"
    class="bg-white absolute w-4/5 md:w-1/2 h-[330px] z-10 left-1/2 translate-x-[-50%] rounded-lg shadow-md"
  >
    <ul class="px-0">
      <li
        class="suggest-li hover:bg-gray-2 text-zinc-7 text-nowrap overflow-clip"
        v-for="suggest in suggestList"
        @click="handleSearch(suggest)"
      >
        {{ suggest }}
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.suggest-li {
  line-height: 30px;
  font-size: 14px;
  padding: 0px 25px;
  cursor: pointer;
  list-style: none;
  transition: 0.3s;
}
</style>
