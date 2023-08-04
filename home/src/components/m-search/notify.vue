<script setup lang="ts">
import { onMounted, ref } from "vue";

defineOptions({
  name: "MNotify",
});
// 第四栏：消息通知
const notifications = ref(["哈哈导航不求最全，但求好用", "我不知道说什么", "通知填充数据"]); // 替换成你的消息通知内容
const currentIndex = ref(0);
const isVisible = ref(true);
// 定时切换消息通知内容的显示
function rotateNotifications() {
  currentIndex.value = (currentIndex.value + 1) % notifications.value.length;
}

// 开始定时切换
onMounted(() => {
  setInterval(rotateNotifications, 3000); // 每3秒切换一次消息通知内容
});

// 隐藏当前通知
function hideNotification() {
  isVisible.value= false;
}
</script>

<template>
  <!-- 第四栏：消息通知 -->
  <div class="flex justify-center" v-if="isVisible">
      <div class="w-1/3 bg-#40085c bg-opacity-45 rounded-full">
        <div v-for="(notification, index) in notifications" :key="index">
          <div
            v-show="currentIndex === index"
            class="flex justify-between items-center py-2 px-4"
          >
            <div class="flex items-center">
              <div class="material-symbols:volume-up-outline w-5 h-5 text-white"></div>
              <span class="text-white text-nowrap overflow-clip w-full h-full text-size-sm ml-2">{{ notification }}</span>
            </div>
            <div @click="hideNotification" class="cursor-pointer opacity-40 hover:opacity-300">
              <div class="mdi:close-circle-outline w-5 h-5 text-white"></div>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<style lang="scss" scoped>

</style>
