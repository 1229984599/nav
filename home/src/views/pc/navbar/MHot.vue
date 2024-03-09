<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { TabsPaneContext } from "element-plus";
import { computed, onMounted, reactive, ref } from "vue";
import { getHotList, HotItemType } from "@/api/spider";
import { isMobile } from "@/utils/window";

defineOptions({
  name: "MHot",
});

const dataList = ref<HotItemType[]>([]);
const targetRef = ref<HTMLElement>();
const isLoading = ref(false);
// 容器宽度
const containerWidth = computed(() => {
  return isMobile.value ? "290" : "420";
});
// tabs列表
const tabsList = [
  { label: "百度", name: "BaiduHot" },
  { label: "B站", name: "BiliBliHot" },
  { label: "微博", name: "WeiBoHot" },
  { label: "抖音", name: "DouYinHot" },
  { label: "搜狗", name: "SoGouHot" },
  { label: "360", name: "SoHot" },
  { label: "头条", name: "TouTiaoHot" },
  { label: "知乎", name: "ZhiHuHot" },
  { label: "快手", name: "KuaiShouHot" },
];
const activeName = ref(tabsList[0].name);
async function handleChangeTabs(tab: TabsPaneContext, event: Event) {
  isLoading.value = true;
  const { name } = tab.props;
  getHotList(String(name))
    .then((res) => {
      dataList.value = res;

      document.querySelector(`#pane-${name} > .hot-container`)?.scrollTo(0, 0);
    })
    .finally(() => {
      isLoading.value = false;
    });
}

onMounted(() => {
  isLoading.value = true;
  getHotList(tabsList[0].name)
    .then((res) => {
      dataList.value = res;
    })
    .finally(() => {
      isLoading.value = false;
    });
});
</script>

<template>
  <el-popover
    placement="bottom-start"
    :width="containerWidth"
    :offset="5"
    trigger="hover"
  >
    <template #default>
      <el-tabs v-model="activeName" @tab-click="handleChangeTabs">
        <el-tab-pane
          :label="tab.label"
          :name="tab.name"
          v-for="tab in tabsList"
        >
          <div v-loading="isLoading" ref="targetRef" class="hot-container">
            <div
              class="hot-item"
              :key="index"
              v-for="(item, index) in dataList"
            >
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
        </el-tab-pane>
      </el-tabs>
    </template>
    <template #reference>
      <div class="flex items-center cursor-pointer">
        <m-icon icon="ph:fire-fill" color="#bb0c0c" />
        <span class="text-sm font-bold text-gray-600">今日热榜</span>
      </div>
    </template>
  </el-popover>
</template>

<style scoped lang="scss">
.hot-container {
  position: relative;
  max-height: 300px;
  overflow-y: auto;
  box-sizing: border-box;
  @mixin overflow-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

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
      width: 23px;
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
</style>
