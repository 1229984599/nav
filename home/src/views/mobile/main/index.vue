<script setup lang="ts">
import MSearch from "@/components/m-search/index.vue";
import MMobileLocalItem from "./item-list/local-item.vue";

defineOptions({
  name: "MMobileMain",
});
</script>

<template>
  <main class="md:w-[90%] lg:w-[80%] xl:w-[70%] mx-auto">
    <m-search font-size="30px" />
    <m-mobile-local-item class="md:mt-4 lg:mt-5" />
  </main>
</template>

<style scoped lang="scss">
main {
  padding: 7% 10% 0;
  @media screen and (max-width: 768px) {
    padding: 20px;
  }
}
</style>
