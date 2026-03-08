<script setup lang="ts">
import { PropType } from "vue";
import { useRouter } from "vue-router";
import SubMenuItem from "@/views/pc/side-menu/SubMenuItem.vue";
import { MenuSchemaTree } from "@/api/menu/types";
import { useMenuStore } from "@/store/menu";

defineProps({
  item: Object as PropType<MenuSchemaTree>,
  iconSize: {
    type: [String, Number],
    default: 25,
  },
});
const router = useRouter();
const menuStore = useMenuStore();

function gotoList(item: MenuSchemaTree) {
  menuStore.setActiveMenuIndex(item.title || "");
  router.push({
    path: "/list",
    query: {
      cat: item.title,
      _t: Date.now().toString(),
    },
    replace: true,
  });
}

function gotoChild(parent: MenuSchemaTree, child: MenuSchemaTree) {
  // 通知 TabCategory 切换到对应子分类 tab
  if (parent.id && child.id) {
    menuStore.setActiveSubTab(parent.id, child.id);
  }
  menuStore.setActiveMenuIndex(child.title || "");
  // 滚动到父分类位置，用 _t 时间戳强制触发路由变化
  router.push({
    path: "/list",
    query: {
      cat: parent.title,
      sub: child.title,
      _t: Date.now().toString(),
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
        <div @click="gotoList(item)">
          <sub-menu-item :item="item" :icon-size="iconSize" />
        </div>
      </template>
      <el-menu-item
        @click="gotoChild(item, submenu)"
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
