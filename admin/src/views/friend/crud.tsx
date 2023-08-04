import { CreateCrudOptionsRet } from "@fast-crud/fast-crud";
import friendModel from "@/api/friend";
import { useRequest } from "@/api/crud";
import { UseIconForm } from "@/hooks/icon";
import { useSpiderButtons } from "@/hooks/spider";
import { useActionButtons } from "@/hooks/crud";

export default function createCrudOptions(crudExpose): CreateCrudOptionsRet {
  const iconForm = UseIconForm(false);
  const { spider } = useSpiderButtons(friendModel);
  const actionButton = useActionButtons(crudExpose, friendModel);
  return {
    crudOptions: {
      request: {
        ...useRequest(friendModel)
      },
      actionbar: {
        buttons: {
          ...actionButton
        }
      },
      form: {
        wrapper: {
          buttons: {
            spider
          }
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
        href: {
          title: "链接",
          type: "text",
          form: {
            order: 0
          }
        },
        desc: {
          title: "描述",
          type: "textarea",
          column: {
            show: false
          },
          form: {
            show: true
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
            width: 180,
            order: 2
          }
        }
      }
    }
  };
}
