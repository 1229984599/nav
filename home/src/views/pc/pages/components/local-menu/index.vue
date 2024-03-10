<script setup lang="ts">
import ItemCategory from "../ItemCategory.vue";
import { useMenuStore } from "@/store/menu";
import MIcon from "@/components/MIcon.vue";
import MLocalAddLink from "./AddLink.vue";
import { ref } from "vue";
import { LinkSchemaList } from "@/api/links/types";
import { ElMessage } from "element-plus";

defineOptions({
  name: "MLocalMenu",
});

const menuStore = useMenuStore();
const linkRef = ref<HTMLElement>();
const isVisible = ref(false);

function handleAddLink() {
  linkRef.value.formRef?.resetFields();
  isVisible.value = true;
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
        <m-icon
          @click="handleAddLink"
          class="cursor-pointer"
          icon="subway:add"
          size="24"
          :color="menuStore.localMenu.color"
        />
      </template>
      <template #local-action="{ item }">
        <div class="local-action">
          <m-icon
            @click.stop="handleEdit(item)"
            size="23"
            color="#409eff"
            icon="mingcute:edit-line"
          />
          <el-popconfirm
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDelete(item)"
            title="确定要删除吗？"
          >
            <template #reference>
              <m-icon
                size="23"
                color="#f56c6c"
                icon="material-symbols:delete-sharp"
              />
            </template>
          </el-popconfirm>
        </div>
      </template>
    </item-category>
    <m-local-add-link ref="linkRef" v-model="isVisible" />
  </div>
</template>

<style scoped lang="scss">
.local-action {
  position: absolute;
  bottom: -3px;
  left: 8px;
  display: flex;
  column-gap: 3px;
  //background-color: ;
  & > div {
    cursor: pointer;
    transition: all 0.23s ease-in-out;
    &:hover {
      box-shadow: rebeccapurple 0 0 10px 0;
    }
    //box-shadow: rebeccapurple 0 0 10px 0;
    //border-radius: 999px;
  }
}
</style>
