<script setup lang="ts">
import { LocationQueryValue, useRoute } from "vue-router";
import { onMounted, ref, watch } from "vue";
import { useMenuStore } from "@/store/menu";
import ItemCategory from "./components/ItemCategory.vue";
import { useTitle } from "@vueuse/core";
import { useSiteStore } from "@/store/site";
import MLocalMenu from "@/components/local-menu/index.vue";
import ItemDesc from "@/views/pc/pages/components/ItemDesc.vue";
import MIcon from "@/components/MIcon.vue";
import { VueDraggable } from "vue-draggable-plus";

const routes = useRoute();
const siteStore = useSiteStore();
const menuStore = useMenuStore();
const linkRef = ref();
function gotoCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  const el = document.querySelector(`#${cat}`);
  if (el) {
    document.querySelector(".right-container")?.scroll({
      top: el?.offsetTop - 90,
      behavior: "smooth",
    });
  }
}

watch(
  () => routes.query?.cat,
  (cat) => {
    useTitle(`${siteStore.siteInfo.title} - ${cat || "首页"}`);
    if (cat) {
      gotoCategory(cat);
    }
  },
);
onMounted(() => gotoCategory(routes.query?.cat));
</script>

<template>
  <div>
    <m-local-menu ref="linkRef">
      <template #item-list>
        <VueDraggable
          class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-x-4 md:gap-x-6 gap-y-4 mb-8 mt-3"
          v-model="menuStore.localMenu.links"
          filter=".add-more"
        >
          <div
            class="item-container"
            :key="item.href"
            v-for="item in menuStore.localMenu.links"
          >
            <item-desc :item="item" />
            <div class="local-action">
              <m-icon
                class="edit-action"
                @click.stop="
                  () => {
                    linkRef?.action?.handleEdit(item);
                  }
                "
                size="23"
                color="#409eff"
                icon="mdi:circle-edit-outline"
              />
              <el-popconfirm
                confirm-button-text="确定"
                cancel-button-text="取消"
                @confirm="
                  () => {
                    linkRef?.action?.handleDelete(item);
                  }
                "
                title="确定要删除吗？"
              >
                <template #reference>
                  <m-icon
                    class="delete-action"
                    size="30"
                    color="#f56c6c"
                    icon="typcn:delete"
                  />
                </template>
              </el-popconfirm>
            </div>
          </div>

          <el-tooltip content="添加本地书签">
            <m-icon
              @click.stop="
                () => {
                  linkRef?.action?.handleAddLink();
                }
              "
              class="add-more w-full"
              icon="ci:file-add"
              size="60"
              :color="menuStore.localMenu.color"
            />
          </el-tooltip>
        </VueDraggable>
      </template>
    </m-local-menu>
    <div v-for="menu in menuStore.menuTree">
      <!--    菜单启用-->
      <item-category :menu="menu" v-if="menu?.status" />
      <!--    有子类并且菜单启用-->
      <div
        class="gap-y-6"
        v-if="menu?.children && menu.children.length > 0 && menu?.status"
      >
        <item-category :menu="subCat" v-for="subCat in menu.children" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.item-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

  &:hover > .local-action {
    visibility: visible;
    opacity: 1;
  }

  .local-action {
    visibility: hidden;
    opacity: 0;
    transition: all 0.3s ease;
    cursor: pointer;

    .edit-action {
      position: absolute;
      bottom: -5px;
      left: 2px;
      background-color: rgba(255, 255, 255, 0.2);
      border-radius: 999px;
      transition: all 0.3s ease;

      &:hover {
        transform: scale(1.3);
        box-shadow: rebeccapurple 0 0 2px 0;
      }
    }

    .delete-action {
      position: absolute;
      right: -0.5rem;
      top: -15px;
      background-color: rgba(255, 255, 255, 0.2);
      border-radius: 999px;
      transition: all 0.3s ease;

      &:hover {
        transform: scale(1.2);
        box-shadow: rebeccapurple 0 0 2px 0;
      }
    }
  }
}
.add-more {
  text-size-adjust: 100%;
  min-width: 160px;
  background-color: var(--el-fill-color-lighter);
  border: 1px dashed var(--el-border-color-darker);
  border-radius: 6px;
  box-sizing: border-box;
  min-height: 79px;
  cursor: pointer;
  vertical-align: top;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;

  &:hover {
    border-color: var(--el-color-primary);
  }
}
</style>
