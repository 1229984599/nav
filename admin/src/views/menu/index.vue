<template>
  <m-table :crud-options="crudOptions" :model="menuModel"></m-table>
</template>

<script lang="ts" setup>
import MTable from "@/components/table/index.vue";
import { CrudOptions, dict } from "@fast-crud/fast-crud";
import { useSpiderButtons } from "@/hooks/spider";
import { UseIconForm } from "@/hooks/icon";
import menuModel from "@/api/menu";

const iconForm = UseIconForm(true);
const { spider } = useSpiderButtons(menuModel);

const crudOptions: CrudOptions = {
  form: {
    wrapper: {
      buttons: {
        spider,
      },
    },
  },
  request: {
    pageRequest: async () => {
      const data = await menuModel.getMenuTree();
      return {
        items: data,
        page: 1,
        pages: 1,
        size: 10,
        total: 10,
      };
    },
  },
  columns: {
    id: {
      column: {
        width: 100,
      },
    },
    title: {
      title: "标题",
      type: "text",
      search: { show: true }, // 开启查询
      form: {
        rules: [{ required: true, message: "请输入标题" }],
      },
      column: {
        width: 180,
      },
    },
    ...iconForm,
    parent_id: {
      title: "父级菜单",
      type: "dict-select",
      column: {
        show: false,
      },
      form: {
        col: { span: 12 },
      },
      dict: dict({
        getData: async () => {
          const { items } = await menuModel.list(
            { size: 100 },
            { parent_id: 0 },
          );
          return items;
        },
        label: "title",
        value: "id",
        immediate: false,
        // data: [{ label: "aa", value: "bb" }]
      }),
    },
    order: {
      title: "排序",
      type: "number",
      column: {
        showTitle: "值越小越靠前",
      },
      form: {
        col: { span: 12 },
      },
    },
    create_time: {
      title: "创建时间",
      type: "datetime",
      form: { show: false, submit: false }, // 表单配置
      viewForm: {
        show: true,
      },
      column: {
        width: 180,
      },
    },
  },
};
</script>
