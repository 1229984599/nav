<template>
  <m-table :crud-options="crudOptions" :model="friendModel"></m-table>
</template>

<script lang="ts" setup>
import MTable from "@/components/table/index.vue";
import { CrudOptions } from "@fast-crud/fast-crud";
import friendModel from "@/api/friend";
import { useSpiderButtons } from "@/hooks/spider";
import { UseIconForm } from "@/hooks/icon";

const iconForm = UseIconForm(friendModel);
const { spider } = useSpiderButtons(friendModel);
const crudOptions: CrudOptions = {
  form: {
    wrapper: {
      buttons: {
        spider,
      },
    },
  },
  columns: {
    title: {
      title: "标题",
      type: "text",
      search: { show: true }, // 开启查询
      column: {
        width: 251,
      },
    },

    ...iconForm,

    href: {
      title: "链接",
      type: "text",
      form: {
        order: 0,
      },
    },
    order: {
      title: "排序",
      type: "number",
      form: {
        col: { span: 6 },
        order: 10,
      },
      column: {
        sortable: "custom",
      },
    },
    desc: {
      title: "描述",
      type: "textarea",
      column: {
        show: false,
      },
      form: {
        show: true,
      },
    },
  },
};
</script>
