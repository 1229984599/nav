import { CreateCrudOptionsRet } from "@fast-crud/fast-crud";
import menuModel from "@/api/menu";
import { useRequest } from "@/api/crud";

export default function createCrudOptions(crudExpose: {
  doRefresh: () => void;
}): CreateCrudOptionsRet {
  return {
    crudOptions: {
      request: {
        ...useRequest(menuModel)
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
        icon: {
          title: "图标",
          type: "text"
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
