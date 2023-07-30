<script lang="ts" setup>
import { defineProps, reactive, ref, useSlots } from "vue"
import {
  VxeGridProps,
  VxeGridInstance,
  VxeFormItemProps,
  VxeGridPropTypes,
  VxeGridListeners,
  VxeToolbarPropTypes
} from "vxe-table"
import Crud from "@/api/crud"
import { filterEmptyKeysAndValues } from "@/utils/validate"

const props = defineProps<{
  crud: Crud
  columns: VxeGridPropTypes.Columns
  searchItems?: VxeFormItemProps[]
  toolbarSlots?: string
}>()
const xGrid = ref({} as VxeGridInstance)
// const whiteList = ['created', 'updated']
// const fields:string[] = <string[]>props.columns.map(item => {
//   if (!whiteList.includes(<string>item.field))
//     return item.field
// })
const gridOptions = reactive<VxeGridProps>({
  border: true,
  height: "auto",
  keepSource: true,
  autoResize: true,
  importConfig: {},
  printConfig: {},
  exportConfig: {},
  formConfig: {
    align: "center",
    items: [
      ...(props.searchItems || []),
      {
        itemRender: {
          name: "$button",
          props: {
            type: "submit",
            content: "查询"
          }
        }
      },
      {
        itemRender: {
          name: "$button",
          props: {
            type: "reset",
            content: "重置"
          }
        }
      }
    ]
  },
  toolbarConfig: {
    buttons: [
      { code: "insert", name: "添加", icon: "Plus", status: "primary" },
      { code: "save", name: "保存", icon: "fa fa-save", status: "success" },
      { code: "delete", name: "删除", icon: "fa fa-trash-o", status: "danger" }
    ],
    // tools: [
    //   props.toolbarTool?.tool || {}
    // ],
    slots: {
      tools: props.toolbarSlots
    },
    export: true,
    print: true,
    import: true,
    custom: true,
    refresh: true
  },
  editConfig: {
    trigger: "click",
    mode: "row",
    showStatus: true
  },
  columns: [{ type: "checkbox", width: 50 }, { type: "seq", width: 60 }, ...props.columns],
  columnConfig: {
    resizable: true
  },
  pagerConfig: {
    pageSize: 10,
    // total: 10,
    background: true,
    align: "center",
    pageSizes: [5, 10, 20, 50, 100]
  },
  proxyConfig: {
    form: true,
    seq: true,
    ajax: {
      // 接收 Promise
      query: async ({ page, form }) => {
        const resp = await props.crud.list(page.currentPage, page.pageSize, form)
        return {
          result: resp.items,
          page: {
            total: resp.total
          }
        }
      },
      save: ({ body }) => {
        const { insertRecords, updateRecords } = body
        insertRecords.map(async (item) => {
          // const insertData = {}
          // fields.forEach(field => {
          //   if (item[field]) {
          //     insertData[field] = item[field];
          //   }
          // })
          return await props.crud.create(filterEmptyKeysAndValues(item))
        })
        updateRecords.map(async (item) => {
          // const updateData = {}
          // fields.forEach(field => {
          //   updateData[field] = item[field]
          // })
          return await props.crud.update(item.id, filterEmptyKeysAndValues(item))
        })
        return Promise.resolve()
      },
      delete: async ({ body }) => {
        const { removeRecords } = body
        const ids = removeRecords.map((item) => item.id).join(",")
        await props.crud.delete(ids)
      }
    }
  }
})
const slots = useSlots()
</script>

<template>
  <vxe-grid ref="xGrid" v-bind="gridOptions" class="p-2">
    <template #[props.toolbarSlots]>
      <slot></slot>
    </template>
  </vxe-grid>
</template>

<style lang="scss" scoped></style>
