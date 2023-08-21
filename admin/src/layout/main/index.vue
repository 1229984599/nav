<script lang="ts">
export default {
  name: "MAppMain",
};
</script>
<script setup lang="ts">
import MTagsView from "./tags-view/index.vue";
import { watch } from "vue";
import { useRoute } from "vue-router";
import { useTagsViewStore } from "@/store";

const tagsViewStore = useTagsViewStore();
const route = useRoute();
watch(
  route,
  (route) => {
    const { meta, path } = route;
    tagsViewStore.addTagsView({
      meta,
      path,
    });
  },
  { immediate: true },
);
</script>

<template>
  <m-tags-view />
  <div class="app-main">
    <router-view v-slot="{ Component, route }">
      <transition name="fade-transform" mode="out-in">
        <keep-alive>
          <component :is="Component" :key="route.path" />
        </keep-alive>
      </transition>
    </router-view>
  </div>
</template>

<style lang="scss" scoped>
@import "@/styles/variables.module.scss";

.app-main {
  min-height: calc(100vh - #{$headerHeight} - 43px);
  width: 100%;
  position: relative;
  padding: 5px;
  overflow: hidden;
  box-sizing: border-box;
}
/* fade-transform */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
