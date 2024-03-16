<script setup lang="ts">
import ItemCategory from "../ItemCategory.vue";
import { useMenuStore } from "@/store/menu";
import MIcon from "@/components/MIcon.vue";
import MLocalAddLink from "./AddLink.vue";
import { ref } from "vue";
import { LinkSchemaList } from "@/api/links/types";
import { ElMessage, ElMessageBox } from "element-plus";

defineOptions({
  name: "MLocalMenu",
});

const menuStore = useMenuStore();
const linkRef = ref<HTMLElement>();
const isVisible = ref(false);

function handleAddLink() {
  linkRef.value?.formRef?.resetFields();
  isVisible.value = true;
}

function handleResetLink() {
  ElMessageBox.confirm("确定要清空本地书签吗？", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "error",
  }).then(() => {
    menuStore.resetLocalLink();
    ElMessage.success("清空成功");
  });
}

function handleEdit(item: LinkSchemaList) {
  Object.assign(linkRef.value?.form, item);
  isVisible.value = true;
}

function handleDelete(item: LinkSchemaList) {
  menuStore.deleteLocalLink(item);
  ElMessage.success("删除成功");
}
</script>

<template>
  <div>
    <item-category :menu="menuStore.localMenu">
      <template #title-action>
        <el-tooltip content="清空本地书签">
          <m-icon
            class="cursor-pointer"
            icon="material-symbols:reset-wrench-rounded"
            :color="menuStore.localMenu.color"
            @click.stop="handleResetLink"
            size="30"
          />
        </el-tooltip>
      </template>
      <template #local-action="{ item }">
        <div class="local-action">
          <m-icon
            class="edit-action"
            @click.stop="handleEdit(item)"
            size="23"
            color="#409eff"
            icon="mdi:circle-edit-outline"
          />
          <el-popconfirm
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDelete(item)"
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
      </template>
      <template #add-more>
        <el-tooltip content="添加本地书签">
          <m-icon
            @click.stop="handleAddLink"
            class="add-more"
            icon="ci:file-add"
            size="60"
          />
        </el-tooltip>
      </template>
    </item-category>
    <m-local-add-link ref="linkRef" v-model="isVisible" />
  </div>
</template>

<style scoped lang="scss">
.local-action {
  cursor: pointer;
  .edit-action {
    position: absolute;
    bottom: -5px;
    left: 2px;
    transition: all 0.3s ease;
    &:hover {
      transform: scale(1.3);
      box-shadow: rebeccapurple 0 0 2px 0;
      border-radius: 999px;
    }
  }
  .delete-action {
    position: absolute;
    right: -0.5rem;
    top: -15px;
    transition: all 0.3s ease;
    &:hover {
      transform: scale(1.2);
      box-shadow: rebeccapurple 0 0 2px 0;
      border-radius: 999px;
    }
  }

  //box-shadow: rebeccapurple 0 0 10px 0;
  //border-radius: 999px;
}

.add-more {
  text-size-adjust: 100%;

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
