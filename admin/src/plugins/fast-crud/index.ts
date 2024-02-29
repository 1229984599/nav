// 引入fast-crud
import {
  CrudBinding,
  CrudOptions,
  FastCrud,
  setLogger,
  useTypes,
} from "@fast-crud/fast-crud";
import "@fast-crud/fast-crud/dist/style.css";

// 请选择ui: element/ antdv /naive。三选一，不支持动态切换
// element
import ui from "@fast-crud/ui-element";
import { App, Component, ref } from "vue";
// @ts-ignore
import { request } from "@/utils/request";
import { registerPlugins } from "./plugins";

// 设置日志级别
setLogger("error");

export function useFastCrud(app: App) {
  // 先安装ui
  app.use(ui);
  // 然后安装FastCrud
  app.use(FastCrud, {
    logger: { off: { tableColumns: false } },
    // 此处配置公共的dictRequest（字典请求）
    async dictRequest(config) {
      // @ts-ignore
      return await request(config); //根据dict的url，异步返回一个字典数组
    },
    //公共crud配置
    commonOptions(): CrudOptions {
      return {
        request: {
          //接口请求配置
          //你项目后台接口大概率与fast-crud所需要的返回结构不一致，所以需要配置此项
          //请参考文档http://fast-crud.docmirror.cn/api/crud-options/request.html
          transformQuery: ({ page, form, sort }) => {
            //转换为你pageRequest所需要的请求参数结构
            const query = {
              params: {
                page: page?.currentPage,
                size: page?.pageSize,
                order_by: "",
              },
              filters: form,
            };
            // debugger;
            if (typeof sort?.asc === "boolean") {
              // @ts-ignore
              query.params.order_by = sort.asc ? sort.prop : `-${sort.prop}`;
            }
            // 修改form中status为
            if (form?.status === "") {
              form.status = null;
            }

            // debugger;

            return query;
          },
          transformRes: ({ res }) => {
            //将pageRequest的返回数据，转换为fast-crud所需要的格式
            //return {records,currentPage,pageSize,total};
            return {
              records: res.items,
              currentPage: res.page,
              pageSize: res.size,
              total: res.total,
            };
            // return { ...res };
          },
        },
        //你可以在此处配置你的其他crudOptions公共配置
        table: {
          editable: {
            enabled: false,
            mode: "free",
            activeTrigger: "onClick",
          },
        },
        rowHandle: {
          fixed: "right",
          align: "center",
          width: 175,
          buttons: {
            edit: {
              icon: "edit",
              text: "",
            },
            view: {
              icon: "view",
              text: "",
            },
            remove: {
              icon: "delete",
              text: "",
            },
          },
        },
        pagination: {
          pageSize: 10,
          background: true,
          // "hide-on-single-page": true,
          "page-sizes": ["5", "10", "20", "50", "100"],
        },
        form: {
          col: {
            span: 24,
          },
        },
        columns: {
          $checked: {
            title: "选择",
            form: { show: false },
            column: {
              type: "selection",
              align: "center",
              width: "55px",
              columnSetDisabled: true, //禁止在列设置中选择
            },
          },
          id: {
            title: "id",
            form: { show: false }, // 表单配置
            column: {
              width: 70,
              // show: false,
            },
          },
        },
      };
    },
  });
  // 注册自定义组件
  registerPlugins();
}
