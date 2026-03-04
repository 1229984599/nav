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
  <header class="mobile-header">
    <div class="header-left flex gap-x-2">
      <m-weather color="white" />
      <m-hot />
    </div>
    <m-yiyan class="yiyan" color="white" />

    <m-profile class="header-profile" color="white" />
  </header>
</template>

<style scoped lang="scss">
.mobile-header {
  margin: 14px 12px 0;
  padding: 10px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.36);
  color: white;
  box-shadow:
    0 10px 22px rgba(5, 14, 35, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.48);
  backdrop-filter: blur(22px) saturate(1.16);
  -webkit-backdrop-filter: blur(22px) saturate(1.16);
  background: linear-gradient(130deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.14));

  &::before {
    content: "";
    width: 52px;
    height: 12px;
    border-radius: 999px;
    margin-right: 10px;
    flex-shrink: 0;
    background: radial-gradient(circle at 6px 50%, #ff5f56 0 4px, transparent 4.5px),
      radial-gradient(circle at 24px 50%, #ffbd2e 0 4px, transparent 4.5px),
      radial-gradient(circle at 42px 50%, #27c93f 0 4px, transparent 4.5px);
  }

  .header-left {
    margin-left: 2px;
  }

  .header-profile {
    margin-left: 12px;
  }

  .yiyan {
    max-width: 54%;
    text-align: center;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.98);
    text-shadow: 0 2px 6px rgba(9, 13, 21, 0.16);
  }
}

@media screen and (max-width: 768px) {
  .mobile-header {
    padding: 9px 10px;
    margin: 10px 10px 0;

    &::before {
      width: 44px;
      margin-right: 8px;
    }

    .yiyan {
      max-width: 48%;
      font-size: 12px;
    }
  }
}
</style>
