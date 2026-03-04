<script setup lang="ts">
import MSearch from "@/components/m-search/index.vue";
import MMobileLocalItem from "./item-list/local-item.vue";

defineOptions({
  name: "MMobileMain",
});
</script>

<template>
  <main class="mobile-main md:w-[90%] lg:w-[80%] xl:w-[70%] mx-auto">
    <section class="search-panel">
      <m-search font-size="30px" />
    </section>
    <m-mobile-local-item class="bookmark-panel md:mt-4 lg:mt-5" />
  </main>
</template>

<style scoped lang="scss">
.mobile-main {
  padding: 7% 10% 0;

  .search-panel {
    padding: 12px 14px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.34);
    background: linear-gradient(140deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.14));
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.46),
      0 9px 22px rgba(4, 12, 32, 0.19);
    backdrop-filter: blur(22px) saturate(1.14);
    -webkit-backdrop-filter: blur(22px) saturate(1.14);
  }

  .bookmark-panel {
    margin-top: 18px;
  }

  @media screen and (max-width: 768px) {
    padding: 20px;

    .search-panel {
      padding: 10px 12px;
      border-radius: 14px;
    }

    .bookmark-panel {
      margin-top: 14px;
    }
  }
}
</style>
