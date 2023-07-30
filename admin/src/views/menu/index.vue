<script setup lang="ts">
import { VxeFormItemProps, VxeGridPropTypes } from "vxe-table"
import TableList from "@/components/TableList/index.vue"
import menu from "@/api/menu"
import XEUtils from "xe-utils"

const columns: VxeGridPropTypes.Columns = [
  {
    field: "title",
    title: "标题",
    editRender: { name: "input" }
  },
  {
    field: "icon",
    title: "图标",
    editRender: { name: "input" }
  },
  {
    field: "created",
    title: "创建时间",
    sortable: true,
    formatter({ cellValue }) {
      return XEUtils.toDateString(cellValue)
    }
  }
]
const searchItems: VxeFormItemProps[] = [
  {
    field: "title",
    itemRender: {
      name: "$input",
      props: {
        placeholder: "查询标题",
        type: "text"
      }
    }
  }
]
</script>

<template>
  <table-list :crud="menu" :columns="columns" :search-items="searchItems" />
</template>

<style scoped></style>
