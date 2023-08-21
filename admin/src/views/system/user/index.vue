<template>
  <m-table :crud-options="crudOptions" :model="userModel"></m-table>
</template>

<script lang="ts" setup>
import MTable from "@/components/table/index.vue";
import { CrudOptions } from "@fast-crud/fast-crud";
import userModel from "@/api/system/user";

const crudOptions: CrudOptions = {
  columns: {
    username: {
      title: "用户名",
      type: "text",
      search: { show: true, autoSearchTrigger: "change" }, // 开启查询,
      addForm: {
        rules: [{ required: true, message: "用户名不能为空" }],
      },
      column: {
        sortable: "custom",
      },
    },
    password: {
      title: "密码",
      type: "text",
      key: "password",
      column: {
        show: false,
      },
      form: {
        rules: [{ min: 5, max: 18, message: "密码必须为5-18位之间" }],
        component: {
          showPassword: true,
        },
        helper: "填写则修改密码",
      },
    },
    nickname: {
      title: "昵称",
      type: "text",
      // search: { show: true }, // 开启查询
      form: {
        rules: [{ max: 50, message: "最大50个字符" }],
      },
      column: {
        sorter: true,
      },
    },
  },
};
</script>
