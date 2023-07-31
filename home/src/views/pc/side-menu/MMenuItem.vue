<script setup lang="ts">
import MIcon from "@/components/MIcon.vue";
import { PropType } from "vue";
import { useRouter } from "vue-router";

defineProps({
  item: Object,
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
        <m-icon size="20" class="pr-1" :icon="item.icon" />
        <span>{{ item.title }}</span>
      </div>
    </template>
    <el-menu-item
      @click="gotoList(submenu)"
      :index="submenu.title"
      v-for="submenu in item.children"
    >
      <m-icon size="20" class="pr-1" :icon="submenu.icon" />
      {{ submenu.title }}
    </el-menu-item>
  </el-sub-menu>
  <el-menu-item @click="gotoList(<MenuType>item)" v-else :index="item?.title">
    <m-icon size="20" class="pr-1" :icon="item?.icon" />
    {{ item.title }}
  </el-menu-item>
</template>

<style scoped></style>
