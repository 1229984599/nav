import {
  asyncCompute,
  compute,
  CreateCrudOptionsRet,
  dict
} from "@fast-crud/fast-crud";
import menuModel from "@/api/menu";
import Crud, { useRequest } from "@/api/crud";
import { UseIconForm } from "@/hooks/icon";
import { ElMessage } from "element-plus";
import { useActionButtons } from "@/hooks/crud";
import { type CrudExpose } from "@fast-crud/fast-crud/dist/d/d/expose";

async function getMenuList(currentId: number) {
  const { items } = await menuModel.list(1, 100);
  // return items;
  return items?.filter(item => item.id !== currentId);
}

export default function createCrudOptions(
  crudExpose: CrudExpose
): CreateCrudOptionsRet {
  const iconForm = UseIconForm();
  const { save, deleteAll } = useActionButtons(crudExpose, menuModel);
  return {
    crudOptions: {
      request: {
        ...useRequest(menuModel),
        pageRequest: async (query: {
          page: number | undefined;
          pageSize: number | undefined;
          filters: {} | undefined;
        }) => {
          const data = await menuModel.getMenuTree();
          return {
            items: data,
            page: 1,
            pages: 1,
            size: 20,
            total: 20
          };
        }
      },
      actionbar: {
        buttons: {
          deleteAll,
          save
        }
      },
      table: {
        editable: {
          enabled: true,
          mode: "free" //模式，free=自由编辑，row=行编辑
        }
      },
      columns: {
        id: {
          title: "id",
          form: { show: false }, // 表单配置
          column: {
            width: 70,
            sorter: true
          }
        },
        title: {
          title: "标题",
          type: "text",
          search: { show: true } // 开启查询
        },
        ...iconForm,
        parent_id: {
          title: "父级菜单",
          type: "dict-select",
          column: {
            show: false
          },
          form: {
            col: { span: 12 }
          },
          dict: dict({
            getData: async ({ row }) => {
              return await getMenuList(row?.id);
            },
            label: "title",
            value: "id",
            immediate: false
            // data: [{ label: "aa", value: "bb" }]
          })
        },
        order: {
          title: "排序",
          type: "number",
          column: {
            showTitle: "值越小越靠前"
          },
          form: {
            col: { span: 12 }
          }
        },
        create_time: {
          title: "创建时间",
          type: "datetime",
          form: { show: false, submit: false }, // 表单配置
          viewForm: {
            show: true
          },
          column: {
            width: 180
          }
        }
      }
    }
  };
}
