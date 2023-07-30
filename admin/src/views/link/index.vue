<script setup lang="ts">
import { VxeFormItemProps, VxeGridPropTypes } from "vxe-table"
import TableList from "@/components/TableList/index.vue"
import linkModel from "@/api/links"
import XEUtils from "xe-utils"
import { useMenuStore } from "@/store/modules/menu"

const menuStore = useMenuStore()

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
    field: "menus",
    title: "菜单",
    formatter: ({ cellValue }) => {
      return cellValue?.map((item) => item.title).join(",")
    },
    editRender: {
      name: "$select",
      props: {
        multiple: true,
        clearable: true,
        filterable: true,
        options: menuStore.menuList,
        "option-props": {
          value: "id",
          label: "title"
        }
      }
    }
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
  <table-list :crud="linkModel" :columns="columns" :search-items="searchItems" />
</template>

<style scoped></style>
