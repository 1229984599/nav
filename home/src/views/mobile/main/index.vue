<script setup lang="ts">
import MSearch from "@/components/m-search/index.vue";
import MMobileLocalItem from "./item-list/local-item.vue";

defineOptions({
  name: "MMobileMain",
});
</script>

<template>
  <main>
    <m-search font-size="30px" class="search" />
    <m-mobile-local-item />
  </main>
</template>

<style scoped lang="scss">
main {
  padding: 60px 60px;
  @media screen and (max-width: 768px) {
    padding: 20px;
  }
}
</style>
