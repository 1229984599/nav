<script setup lang="ts">
import { PropType } from "vue";
import { useRouter } from "vue-router";
import SubMuneItem from "@/views/pc/side-menu/SubMuneItem.vue";

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
        <sub-mune-item :item="item" :icon-size="iconSize" />
      </div>
    </template>
    <el-menu-item
      @click="gotoList(submenu)"
      :index="submenu.title"
      v-for="submenu in item.children"
    >
      <sub-mune-item :item="submenu" :icon-size="iconSize" />
    </el-menu-item>
  </el-sub-menu>
  <el-menu-item @click="gotoList(item)" v-else :index="item?.title">
    <sub-mune-item :item="item" :icon-size="iconSize" />
  </el-menu-item>
</template>

<style scoped></style>
