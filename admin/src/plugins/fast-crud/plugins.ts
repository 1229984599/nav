import { useColumns, ColumnCompositionProps } from "@fast-crud/fast-crud";
import { merge } from "lodash-es";

// 跟上面一样，不要写在页面里，这个也是全局的，要写在vue.use(FastCrud)之后

const { registerMergeColumnPlugin } = useColumns();

export function registerPlugins() {
  registerMergeColumnPlugin({
    name: "readonly-plugin",
    order: 1,
    handle: (
      columnProps: ColumnCompositionProps = {},
      crudOptions: any = {},
    ) => {
      // 移动端在table中不显示该字段
      // if (columnProps.response && isMobile.value) {
      //   merge(columnProps, {
      //     column: { show: false },
      //   });
      // }
      // 比如你可以定义一个readonly的公共属性，处理该字段只读，不能编辑
      if (columnProps.readonly) {
        // 合并column配置
        merge(columnProps, {
          form: { show: false, submit: false },
          viewForm: { show: true },
        });
      }
      return columnProps;
    },
  });
}
