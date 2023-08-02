import {
  asyncCompute,
  compute,
  CreateCrudOptionsRet,
  dict
} from "@fast-crud/fast-crud";
import menuModel from "@/api/menu";
import Crud, { useRequest } from "@/api/crud";
import { UseIconForm } from "@/hooks/icon";

async function getMenuList(currentId: number) {
  const { items } = await menuModel.list(1, 100);
  // return items;
  return items?.filter(item => item.id !== currentId);
}

export default function createCrudOptions(crudExpose: {
  doRefresh: () => void;
}): CreateCrudOptionsRet {
  const iconForm = UseIconForm();
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
            total: 100
          };
        }
      },
      form: {
        col: { span: 24 }
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
          editForm: {
            col: { span: 12 }
          },
          dict: dict({
            getData: async ({ row }) => {
              debugger;
              return await getMenuList(row?.id);
            },
            label: "title",
            value: "id",
            immediate: false
            // data: [{ label: "aa", value: "bb" }]
          })
        }
        // created: {
        //   title: "创建时间",
        //   type: "datetime",
        //   form: { show: false, submit: false }, // 表单配置
        //   viewForm: {
        //     show: true
        //   },
        //   column: {
        //     width: 180
        //   }
        // }
      }
    }
  };
}
