<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { getHotList } from "@/api/spider";
import { useScroll } from "@vueuse/core";
import MIcon from "@/components/MIcon.vue";
import { HotItemType } from "@/api/spider/types";

defineOptions({
  name: "MHotItem",
});
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  activeName: {
    type: String,
    required: true,
  },
});
const isLoading = ref(false);
// 当前tab是否激活
const isActive = computed(() => {
  return props.activeName === props.name;
});

const dataList = ref<HotItemType[]>([]);
const targetRef = ref<HTMLElement>();
const { y } = useScroll(targetRef);
// 是否显示回到顶部按钮
const isShowBackTop = computed(() => {
  // console.log(y.value);
  return isActive.value && y.value > 180;
});

function handleBackTop() {
  targetRef.value?.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

function getDataList() {
  return new Promise((resolve) => {
    isLoading.value = true;
    getHotList(props.activeName)
      .then((res) => {
        dataList.value = res;
        resolve(res);
      })
      .finally(() => {
        isLoading.value = false;
      });
  });
}

async function handleChangeTabs() {
  getDataList().then(handleBackTop);
}

// const debounceHandleChangeTabs = useDebounceFn(handleChangeTabs, 500);
watch(
  () => props.activeName,
  () => {
    // debugger;
    if (isActive.value && dataList.value.length === 0) {
      handleChangeTabs();
    }
  },
);
onMounted(() => {
  // 默认只请求当前激活tab
  if (!isActive.value) {
    return;
  }
  getDataList();
});
</script>

<template>
  <el-tab-pane class="relative" :label="label" :name="name">
    <div v-loading="isLoading" ref="targetRef" class="hot-container">
      <div class="hot-item" :key="index" v-for="(item, index) in dataList">
        <div class="flex w-[80%] md:w-[85%] gap-x-2">
          <!--              排行榜序号-->
          <div class="hot-index">{{ index + 1 }}</div>
          <a class="hot-item-title" :href="item.url" target="_blank">{{
            item.title
          }}</a>
        </div>

        <!--              点击数量-->
        <span class="hot-num">{{ item.hot }}</span>
      </div>
    </div>
    <m-icon
      v-show="isShowBackTop"
      @click="handleBackTop"
      class="back-top"
      :size="20"
      icon="bi:rocket-fill"
    />
  </el-tab-pane>
</template>

<style lang="scss" scoped>
.hot-container {
  @mixin overflow-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  position: relative;
  height: 300px;
  max-height: 300px;
  overflow-y: auto;
  box-sizing: border-box;

  & > .hot-item:first-child .hot-index {
    background-color: #fe2d46;
  }

  & > .hot-item:nth-of-type(2) .hot-index {
    background-color: #f60;
  }

  & > .hot-item:nth-of-type(3) .hot-index {
    background-color: #faa90e;
  }

  .hot-item {
    display: flex;
    flex-direction: row;
    width: 100%;
    //cursor: pointer;
    justify-content: space-between;
    align-items: center;
    margin: 8px 0;

    & .hot-index {
      //box-sizing: content-box;
      flex-shrink: 0;
      min-width: 2em;
      padding: 3px;
      font-size: 10px;
      background-color: #1f2d3d;
      color: white;
      text-align: center;
      vertical-align: middle;
      white-space: nowrap;
      border-radius: 3px;
    }

    & .hot-item-title {
      cursor: pointer;
      text-align: start;
      font-weight: 500;
      font-size: 15px;
      //width: 100%;
      //display: inline-block;
      @include overflow-ellipsis;
      transition: color 0.3s ease;

      &:hover {
        color: #f3434e;
      }
    }

    & .hot-num {
      font-size: 12px;
      padding-right: 2px;
      flex-shrink: 0;
      @include overflow-ellipsis;
    }
  }
}
.back-top {
  cursor: pointer;
  position: absolute;
  right: 10px;
  bottom: 10px;
  color: white;
  background-color: #4091f7;
  padding: 4px;
  justify-content: center;
  align-items: center;
  z-index: 100;
  border-radius: 999px;
  transition: background-color 0.2s ease-in-out;

  &:hover {
    background-color: #fe2d46;
  }
}
</style>
