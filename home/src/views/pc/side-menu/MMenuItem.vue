<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { PropType } from "vue";
import { useRouter } from "vue-router";

defineProps({
  item: Object,
  iconSize: {
    type: [String, Number],
    default: 25,
  },
});
const router = useRouter();

function gotoList(item: any) {
  router.push({
    path: "/list",
    query: {
      cat: item.title,
    },
  });
}
</script>

<template>
  <!--  如果有子类-->
  <el-sub-menu
    :index="item.title"
    v-if="item?.children && item.children.length > 0"
  >
    <template #title>
      <div @click="gotoList(item)" class="flex">
        <m-icon
          :size="iconSize"
          class="pr-1"
          :color="item.color"
          :icon="item.icon"
        />
        <span>{{ item.title }}</span>
      </div>
    </template>
    <el-menu-item
      @click="gotoList(submenu)"
      :index="submenu.title"
      v-for="submenu in item.children"
    >
      <m-icon
        :color="submenu.color"
        :size="iconSize"
        class="pr-1"
        :icon="submenu.icon"
      />
      {{ submenu.title }}
    </el-menu-item>
  </el-sub-menu>
  <el-menu-item @click="gotoList(item)" v-else :index="item?.title">
    <m-icon
      :size="iconSize"
      class="pr-1"
      :color="item.color"
      :icon="item?.icon"
    />
    <span class="text-zinc-800 font-bold">
      {{ item.title }}
    </span>
  </el-menu-item>
</template>

<style scoped></style>
