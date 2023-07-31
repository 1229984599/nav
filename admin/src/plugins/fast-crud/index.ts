// 引入fast-crud
import { FastCrud } from "@fast-crud/fast-crud";
import "@fast-crud/fast-crud/dist/style.css";

// 请选择ui: element/ antdv /naive。三选一，不支持动态切换
// element
import ui from "@fast-crud/ui-element";
import { App, Component, ref } from "vue";
import { http } from "@/utils/http";

export function useFastCrud(app: App) {
  // 先安装ui
  app.use(ui);
  // 然后安装FastCrud
  app.use(FastCrud, {
    // 此处配置公共的dictRequest（字典请求）
    async dictRequest(config) {
      // @ts-ignore
      return await http.request(config); //根据dict的url，异步返回一个字典数组
    },
    //公共crud配置
    commonOptions() {
      return {
        request: {
          //接口请求配置
          //你项目后台接口大概率与fast-crud所需要的返回结构不一致，所以需要配置此项
          //请参考文档http://fast-crud.docmirror.cn/api/crud-options/request.html
          transformQuery: ({ page, form, sort }) => {
            //转换为你pageRequest所需要的请求参数结构
            return {
              page: page.currentPage,
              pageSize: page.pageSize,
              filters: form
            };
          },
          transformRes: ({ res }) => {
            //将pageRequest的返回数据，转换为fast-crud所需要的格式
            //return {records,currentPage,pageSize,total};
            return {
              records: res.items,
              currentPage: res.page,
              pageSize: res.size,
              total: res.total
            };
            // return { ...res };
          }
        },
        //你可以在此处配置你的其他crudOptions公共配置
        rowHandle: {
          align: "center",
          buttons: {
            view: {
              icon: "View",
              text: ""
            },
            edit: {
              icon: "edit",
              text: ""
            },
            remove: {
              icon: "delete",
              text: ""
            }
          }
        },
        pagination: {
          pageSize: 10
        },

        columns: {
          $checked: {
            title: "选择",
            form: { show: false },
            column: {
              type: "selection",
              align: "center",
              width: "55px",
              columnSetDisabled: true //禁止在列设置中选择
            }
          }
        },
        // actionbar: {
        //   buttons: {
        //     sync: {
        //       text: "批量删除",
        //       type: "danger",
        //       click: context => {
        //         debugger
        //         console.log(context);
        //       }
        //     }
        //   }
        // }
      };
    }
  });
}
