<template>
  <m-table :crud-options="crudOptions" :model="linkModel"></m-table>
</template>

<script lang="tsx" setup>
import MTable from "@/components/table/index.vue";
import { Icon } from "@iconify/vue";
import { CrudOptions, dict } from "@fast-crud/fast-crud";
import linkModel from "@/api/links";
import { useSpiderButtons } from "@/hooks/spider";
import { UseIconForm } from "@/hooks/icon";
import { useMenuStore } from "@/store";

const iconForm = UseIconForm(linkModel, true);
const { spider } = useSpiderButtons(linkModel);
const menuStore = useMenuStore();

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
      search: {
        show: true,
        component: {
          props: {
            placeholder: "请输入标题",
            clearable: true,
          },
        },
      }, // 开启查询
      form: {
        rules: [{ required: true, message: "请输入标题" }],
      },
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
        rules: [{ required: true, message: "请输入链接" }],
        helper: "输入链接后，点击采集即可自动获取数据",
      },
      column: {
        width: 251,
      },
      search: {
        show: true,
        component: {
          props: {
            placeholder: "请输入链接",
            clearable: true,
          },
        },
      },
    },
    menus: {
      title: "菜单",
      type: "dict-tree",
      valueBuilder(context) {
        // @ts-ignore
        context.row.menus = context.row.menus.map((item) => item.id);
      },
      search: {
        show: true,
      },
      form: {
        col: { span: 14 },
        rules: [{ required: true, message: "菜单为必选项" }],
        render(scope) {
          return (
            <el-tree-select
              v-model={scope.form.menus}
              data={menuStore.menuTree}
              multiple={true}
              render-after-expand={false}
              show-checkbox={true}
              check-strictly={true}
              highlight-current={true}
              filterable={true}
              clearable={true}
              check-on-click-node={true}
              placeholder="请选择"
              class="w-full"
              props={{
                label: "title",
                value: "id",
              }}
              node-key="id"
              value-key="id"
            >
              {{
                default: ({ data }) => {
                  // debugger;
                  return (
                    <div class="flex gap-x-1">
                      <Icon color={data?.color} icon={data?.icon} />
                      <span>{data.title}</span>
                    </div>
                  );
                },
              }}
            </el-tree-select>
          );
        },
      },
      dict: dict({
        // url: "/sys/authority/role/list",
        getData: menuStore.getMenuTree,
        value: "id",
        label: "title",
        isTree: true,
        // immediate: true,
      }),
      column: {
        width: 210,
        component: {
          color: "auto",
        },
      },
    },
    is_self: {
      title: "站内打开",
      column: {
        width: 90,
        show: false,
      },
      form: {
        col: { span: 6 },
      },
      type: "dict-switch",
      dict: dict({
        data: [
          { value: true, label: "是" },
          { value: false, label: "否" },
        ],
      }),
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
    order: {
      title: "排序",
      type: "number",
      form: {
        col: { span: 6 },
      },
      column: {
        sortable: "custom",
      },
    },
    is_vip: {
      title: "是否vip",
      type: "dict-switch",
      column: {
        width: 160,
      },
      form: {
        col: { span: 6 },
      },
      dict: dict({
        data: [
          { value: true, label: "是" },
          { value: false, label: "否" },
        ],
      }),
    },
  },
};
</script>
