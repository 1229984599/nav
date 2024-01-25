import { CreateCrudOptionsRet, dict } from "@fast-crud/fast-crud";
import Crud, { useRequest } from "@/api/crud";
import { useActionButtons } from "./hooks";
import { type CrudExpose } from "@fast-crud/fast-crud/dist/d/d/expose";

export default function createCrudOptions(
  crudExpose: CrudExpose,
  model: Crud,
): CreateCrudOptionsRet {
  const { save, deleteAll } = useActionButtons(crudExpose, model);
  return {
    crudOptions: {
      request: {
        ...useRequest(model),
      },
      actionbar: {
        buttons: {
          deleteAll,
          save,
        },
      },
      columns: {
        status: {
          title: "状态",
          type: "dict-switch",
          column: {
            width: 180,
            order: 100,
          },
          search: {
            show: true,
            order: 100,
          },
          form: {
            rules: [{ required: true, message: "请选择状态" }],
            col: { span: 6 },
            order: 2,
          },
          dict: dict({
            data: [
              { value: true, label: "启用" },
              { value: false, label: "禁用" },
            ],
          }),
        },
        create_time: {
          title: "创建时间",
          type: "datetime",
          readonly: true,
          column: {
            width: 180,
            order: 1001,
            sortable: "custom",
            // show: false,
          },
        },
      },
    },
  };
}
