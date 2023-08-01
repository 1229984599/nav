import { CreateCrudOptionsRet, dict } from "@fast-crud/fast-crud";
import linkModel from "@/api/links";
import { useRequest } from "@/api/crud";
import { useMenuStore } from "@/store/modules/menu";
import { ref } from "vue";
import { message } from "@/utils/message";
import { ElMessageBox } from "element-plus";
import { UseIconForm } from "@/hooks/icon";

const menuStore = useMenuStore();
export default function createCrudOptions(crudExpose: {
  doRefresh: () => void;
}): CreateCrudOptionsRet {
  const selectedIds = ref([]);
  const spiderLoading = ref(false);
  const iconForm = UseIconForm(false);
  return {
    crudOptions: {
      request: {
        ...useRequest(linkModel)
      },
      actionbar: {
        buttons: {
          deleteAll: {
            text: "批量删除",
            type: "danger",
            click: context => {
              ElMessageBox.confirm("确定要批量删除吗？").then(() => {
                linkModel.delete(selectedIds.value.join(",")).then(() => {
                  crudExpose.doRefresh();
                  message("删除成功", { type: "success" });
                });
              });
            }
          }
        }
      },
      form: {
        wrapper: {
          buttons: {
            spider: {
              text: "采集",
              type: "success",
              loading: spiderLoading,
              click: async ({ form }) => {
                spiderLoading.value = true;
                const data = await linkModel.getSiteInfo(form.href);
                Object.assign(form, data);
                spiderLoading.value = false;
              }
            }
          }
        },
        col: {
          span: 24
        }
      },
      table: {
        onSelectionChange: (changed: any[]) => {
          selectedIds.value = changed.map(item => item.id);
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
        is_self: {
          title: "站内打开",
          column: {
            width: 90
          },
          type: "dict-switch",
          dict: dict({
            data: [
              { value: true, label: "是" },
              { value: false, label: "否" }
            ]
          })
        },
        menus: {
          title: "菜单",
          type: "dict-select",
          search: {
            show: true
          },
          form: {
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
        desc: {
          title: "描述",
          type: "textarea",
          column: {
            show: false
          },
          form: {
            show: true
          }
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
