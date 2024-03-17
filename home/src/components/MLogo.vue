<script setup lang="ts">
import { useSiteStore } from "@/store/site";
import MIcon from "@/components/MIcon.vue";
import { useRouter } from "vue-router";
import { onMounted } from "vue";

defineProps({
  fontSize: {
    type: String,
    default: "20px",
  },
});
const siteStore = useSiteStore();
const router = useRouter();

function handleClick() {
  router
    .push({
      name: "List",
    })
    .then(() => {
      // @ts-ignore
      document.querySelector(".right-container").scroll({
        top: 0,
        behavior: "smooth",
      });
    });
}

onMounted(async () => {
  // 如果没有siteinfo数据，就获取重新获取
  if (!siteStore.siteInfo?.id) {
    await siteStore.getSiteInfo();
  }
});
</script>

<template>
  <div class="layout-logo-container px-5">
    <a
      @click="handleClick"
      key="collapse"
      class="flex cursor-pointer decoration-none items-center justify-center"
    >
      <m-icon
        :icon="siteStore.siteInfo?.icon"
        :size="40"
        :color="siteStore.siteInfo?.color"
      />
      <span class="logo-title" :style="{ color: siteStore.siteInfo?.color }">{{
        siteStore.siteInfo?.title
      }}</span>
    </a>
  </div>
</template>

<style lang="scss" scoped>
@import "@/styles/variables.module";

.layout-logo-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
  text-align: center;
  height: #{$navHeaderHeight};

  .logo-title {
    display: block;
    font-family:
      Avenir,
      Helvetica Neue,
      Arial,
      Helvetica,
      sans-serif;
    padding-left: 2px;
    font-size: v-bind(fontSize);
    font-weight: 700;
    overflow: hidden;
    text-align: left;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
