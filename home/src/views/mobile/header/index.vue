<script setup lang="ts">
import MWeather from "@/components/weather/index.vue";
import MProfile from "@/components/MProfile.vue";
import MYiyan from "@/components/MYiyan.vue";
import MHot from "@/components/hot/index.vue";

defineOptions({
  name: "MMobileHeader",
});
</script>

<template>
  <header>
    <div class="flex gap-x-2">
      <m-weather color="white" />
      <m-hot />
    </div>
    <m-yiyan class="yiyan" color="white" />

    <m-profile color="white" />
  </header>
</template>

<style scoped lang="scss">
header {
  padding: 20px 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  backdrop-filter: blur(20px);

  .yiyan {
    max-width: 60%;

    text-align: center;
  }
}
</style>
