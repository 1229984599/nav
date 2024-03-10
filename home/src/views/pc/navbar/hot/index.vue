<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { computed, ref } from "vue";
import { isMobile } from "@/utils/window";
import MHotItem from "./HotItem.vue";

defineOptions({
  name: "MHot",
});

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
  { label: "贴吧", name: "BaiduTieBaHot" },
];
const activeName = ref(tabsList[0].name);
</script>

<template>
  <el-popover
    placement="bottom-start"
    :width="containerWidth"
    :offset="5"
    trigger="hover"
  >
    <template #default>
      <el-tabs v-model="activeName">
        <m-hot-item
          :active-name="activeName"
          :name="tab.name"
          :label="tab.label"
          v-for="tab in tabsList"
        />
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

<style scoped lang="scss"></style>
