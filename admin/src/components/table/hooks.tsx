import { ElMessage, ElMessageBox } from "element-plus";
import {
  ActionbarClickEvent,
  ButtonsProps,
} from "@fast-crud/fast-crud/dist/d/d/crud";
import { type CrudExpose } from "@fast-crud/fast-crud/dist/d/d/expose";
// @ts-ignore
import Crud from "@/api/crud";

export function useActionButtons(
  crudExpose: CrudExpose,
  model: Crud,
): ButtonsProps<ActionbarClickEvent> {
  return {
    save: {
      text: "保存",
      type: "success",
      click: () => {
        // @ts-ignore
        crudExpose.getTableRef().editable.submit(async ({ changed }) => {
          console.log("changed", changed);
          if (changed.length > 0) {
            // @ts-ignore
            const updatePromises = changed.map(async (item) => {
              await model.update(item.id, item);
            });
            // 等待所有更新操作完成
            await Promise.all(updatePromises);
            ElMessage.success("保存成功");

            await crudExpose.doRefresh();
            // setData({ 0: {id:1} }); //设置data
          } else {
            ElMessage.warning("没有数据需要保存");
          }
        });
      },
    },
    deleteAll: {
      text: "批量删除",
      type: "danger",
      click: () => {
        ElMessageBox.confirm("确定要批量删除吗？").then(async () => {
          const selected = crudExpose
            .getTableRef()
            .tableRef.getSelectionRows()
            .map((item: { id: any }) => item.id);
          if (selected.length > 0) {
            model.delete(selected.join(",")).then(async () => {
              await crudExpose.doRefresh();
              ElMessage.success("删除成功");
            });
          } else {
            ElMessage.error("请选择要删除的数据");
          }
        });
      },
    },
  };
}
