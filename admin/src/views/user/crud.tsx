import { CreateCrudOptionsRet, dict } from "@fast-crud/fast-crud";
import userModel from "@/api/user";
import { useRequest } from "@/api/crud";
import { useActionButtons } from "@/hooks/crud";
import { type CrudExpose } from "@fast-crud/fast-crud/dist/d/d/expose";

export default function createCrudOptions(
  crudExpose: CrudExpose
): CreateCrudOptionsRet {
  const { save, deleteAll } = useActionButtons(crudExpose, userModel);
  return {
    crudOptions: {
      request: {
        ...useRequest(userModel)
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
        username: {
          title: "用户名",
          type: "text",
          search: { show: true } // 开启查询
        },
        password: {
          title: "密码",
          type: "text",
          key: "password",
          column: {
            show: false
          },
          form: {
            rules: [{ min: 5, max: 18, message: "密码必须为5-18位之间" }],
            component: {
              showPassword: true
            },
            helper: "填写则修改密码"
          }
        },
        nickname: {
          title: "昵称",
          type: "text",
          // search: { show: true }, // 开启查询
          form: {
            rules: [{ max: 50, message: "最大50个字符" }]
          },
          column: {
            sorter: true
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
