<script setup lang="ts">
import { useMenuStore } from "@/store/menu";
import MIcon from "@/components/MIcon.vue";
import MLocalAddLink from "@/components/add-link/local.vue";
import { ref } from "vue";
import { LinkSchemaList } from "@/api/links/types";
import { ElMessage, ElMessageBox } from "element-plus";

defineOptions({
  name: "MLocalMenu",
});

const menuStore = useMenuStore();
const linkRef = ref();
const isVisible = ref(false);

// 拖拽排序

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

defineExpose({
  action: {
    handleAddLink,
    handleResetLink,
    handleEdit,
    handleDelete,
  },
});
</script>

<template>
  <div>
    <slot name="menu-title" :menu="menuStore.localMenu">
      <div :id="menuStore.localMenu.title" class="flex gap-x-2 items-center">
        <m-icon
          v-if="menuStore.localMenu.icon"
          :style="{ color: menuStore.localMenu.color }"
          :icon="menuStore.localMenu.icon"
        />
        <h2 class="text-xl font-bold">{{ menuStore.localMenu.title }}</h2>

        <el-tooltip content="清空本地书签">
          <m-icon
            class="cursor-pointer"
            icon="material-symbols:reset-wrench-rounded"
            :color="menuStore.localMenu.color"
            @click.stop="handleResetLink"
            size="30"
          />
        </el-tooltip>
      </div>
    </slot>
    <slot name="item-list"></slot>

    <m-local-add-link ref="linkRef" v-model="isVisible" />
  </div>
</template>

<style scoped lang="scss"></style>
