<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getYiyan } from "@/api/spider";

const yiyan = ref("");

async function refresh() {
  const { hitokoto, from } = await getYiyan();
  yiyan.value = `${hitokoto}\t——${from}`;
}

onMounted(refresh);
</script>

<template>
  <span class="yiyan" @click="refresh"
    >{{
      yiyan
    }}fdsddsfsdaf几点开始了几分道理的撒娇的的撒酒疯拉萨大家奥利弗就是大家了的撒酒疯绿豆沙逻辑上的了解多少了房间都是垃圾发来的数据临时搭建陆军第十六进来撒就爱上邓丽君fajdslfjasdlkjfd</span
  >
</template>

<style lang="scss" scoped>
.yiyan {
  display: none;
  cursor: pointer;
  font-size: 0.87rem;
  line-height: 1.25rem;
  color: rgb(82 82 91 /1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  //pc端
  @media (min-width: 768px) {
    display: block;
  }
}
</style>
