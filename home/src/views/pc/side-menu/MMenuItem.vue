<script setup lang="ts">
import { PropType } from "vue";
import { useRouter } from "vue-router";
import SubMenuItem from "@/views/pc/side-menu/SubMenuItem.vue";
import { MenuSchemaTree } from "@/api/menu/types";

defineProps({
  item: Object as PropType<MenuSchemaTree>,
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
    replace: true,
  });
}
</script>

<template>
  <!--  如果有子类-->
  <div v-if="item?.status">
    <el-sub-menu
      :index="item.title"
      v-if="item?.children && item.children.length > 0"
    >
      <template #title>
        <div @click="gotoList(item)" class="flex">
          <sub-menu-item :item="item" :icon-size="iconSize" />
        </div>
      </template>
      <el-menu-item
        @click="gotoList(submenu)"
        :index="submenu.title"
        v-for="submenu in item.children"
      >
        <sub-menu-item :item="submenu" :icon-size="iconSize" />
      </el-menu-item>
    </el-sub-menu>
    <el-menu-item @click="gotoList(item)" v-else :index="item?.title">
      <sub-menu-item :item="item" :icon-size="iconSize" />
    </el-menu-item>
  </div>
</template>

<style scoped></style>
