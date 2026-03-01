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
import { useUserStore } from "@/store/user";
import menu from "@/api/menu";

const routes = useRoute();
const siteStore = useSiteStore();
const menuStore = useMenuStore();
const userStore = useUserStore();
const linkRef = ref();

const isAdmin = ref(!!userStore.token?.access_token);

function gotoCategory(cat: LocationQueryValue | LocationQueryValue[]) {
  if (!cat || typeof cat !== 'string') return;
  const el = document.getElementById(cat);
  if (el) {
    document.querySelector(".right-container")?.scroll({
      top: el.offsetTop - 90,
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

async function handleMenuDragEnd() {
  // 收集所有菜单（父+子）的新排序
  const updates: Array<{ id: number; order: number }> = [];
  menuStore.menuTree.forEach((item, index) => {
    if (item.id) {
      updates.push({ id: item.id, order: index });
    }
    // 子菜单保持原有顺序不变，只排父级
  });
  if (updates.length === 0) return;
  try {
    await menu.batchUpdate(updates);
    await menuStore.getMenuTree();
  } catch (e) {
    console.error("菜单排序保存失败", e);
  }
}
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

    <VueDraggable
      v-if="isAdmin"
      v-model="menuStore.menuTree"
      handle=".menu-drag-handle"
      :animation="150"
      @end="handleMenuDragEnd"
    >
      <div v-for="menuItem in menuStore.menuTree" :key="menuItem.id">
        <!--    菜单启用-->
        <item-category :menu="menuItem" v-if="menuItem?.status" />
        <!--    有子类并且菜单启用-->
        <div
          class="gap-y-6"
          v-if="menuItem?.children && menuItem.children.length > 0 && menuItem?.status"
        >
          <item-category :menu="subCat" v-for="subCat in menuItem.children" :key="subCat.id" />
        </div>
      </div>
    </VueDraggable>

    <template v-else>
      <div v-for="menuItem in menuStore.menuTree">
        <!--    菜单启用-->
        <item-category :menu="menuItem" v-if="menuItem?.status" />
        <!--    有子类并且菜单启用-->
        <div
          class="gap-y-6"
          v-if="menuItem?.children && menuItem.children.length > 0 && menuItem?.status"
        >
          <item-category :menu="subCat" v-for="subCat in menuItem.children" />
        </div>
      </div>
    </template>
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
