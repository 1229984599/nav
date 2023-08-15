import { CreateCrudOptionsRet, dict } from "@fast-crud/fast-crud";
import linkModel from "@/api/links";
import { useRequest } from "@/api/crud";
import { useMenuStore } from "@/store/modules/menu";
import { UseIconForm } from "@/hooks/icon";
import { useSpiderButtons } from "@/hooks/spider";
import { useActionButtons } from "@/hooks/crud";

const menuStore = useMenuStore();
export default function createCrudOptions(crudExpose): CreateCrudOptionsRet {
  const iconForm = UseIconForm(false);
  const { spider } = useSpiderButtons(linkModel);
  const actionButton = useActionButtons(crudExpose, linkModel);
  return {
    crudOptions: {
      request: {
        ...useRequest(linkModel)
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
      table: {
        editable: {
          enabled: true
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
          search: { show: true }, // 开启查询
          form: {
            rules: [{ required: true, message: "请输入标题" }]
          }
        },
        ...iconForm,
        href: {
          title: "链接",
          type: "text",
          form: {
            order: 0,
            rules: [{ required: true, message: "请输入链接" }],
            helper: "输入链接后，点击采集即可自动获取数据"
          }
        },
        menus: {
          title: "菜单",
          type: "dict-select",
          search: {
            show: true
          },
          form: {
            col: { span: 14 },
            rules: [{ required: true, message: "菜单为必选项" }],
            component: {
              multiple: true
            }
          },
          column: {
            component: {
              color: "auto"
            }
          },
          dict: dict({
            // url: "/sys/authority/role/list",
            getData: menuStore.getMenuList,
            value: "id",
            label: "title",
            immediate: true
          })
        },
        is_self: {
          title: "站内打开",
          column: {
            width: 90,
            show: false
          },
          form: {
            col: { span: 6 }
          },
          type: "dict-switch",
          dict: dict({
            data: [
              { value: true, label: "是" },
              { value: false, label: "否" }
            ]
          })
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
        order: {
          title: "排序",
          type: "number",
          form: {
            col: { span: 14 }
          }
        },
        is_vip: {
          title: "是否vip",
          type: "dict-switch",
          column: {
            width: 160
          },
          form: {
            col: { span: 6 }
          },
          dict: dict({
            data: [
              { value: true, label: "是" },
              { value: false, label: "否" }
            ]
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
