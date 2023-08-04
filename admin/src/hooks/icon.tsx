import { ref } from "vue";
import { CompositionColumns } from "@fast-crud/fast-crud/dist/d/d/crud";
import MIcon from "@/components/MIcon.vue";

export function UseIconForm(showUrl: boolean = true): CompositionColumns {
  const iconColor = ref("");
  return {
    icon: {
      title: "图标",
      type: "text",
      column: {
        // width: showUrl ? "auto" : 100,
        cellRender(scope) {
          return (
            <div class="flex items-center gap-x-2">
              <MIcon
                color={scope.row.color}
                icon={scope.value}
                size={30}
              ></MIcon>
              <div>{showUrl ? <span>{scope.value}</span> : <span></span>}</div>
            </div>
          );
        }
      },
      form: {
        col: { span: 18 },
        helper: {
          render: () => {
            return (
              <a href="https://icon-sets.iconify.design/" target="_blank">
                点我前往iconify查看图标
              </a>
            );
          }
        },
        suffixRender(scope) {
          return (
            <div class="flex items-center">
              <MIcon
                style={{ color: iconColor.value || scope.row.color }}
                icon={scope.value}
              ></MIcon>
            </div>
          );
        }
      }
    },
    color: {
      title: "颜色",
      type: "text",
      column: {
        show: false
      },
      form: {
        col: { span: 4 },
        component: {
          name: "el-color-picker",
          props: {
            // value: "#ff4500",
            predefine: [
              "#ff4500",
              "#ff8c00",
              "#ffd700",
              "#90ee90",
              "#00ced1",
              "#1e90ff",
              "#c71585",
              "#c7158577"
            ]
          }
        },
        // @ts-ignore
        valueChange({ value }) {
          iconColor.value = value;
        }
      }
    }
  };
}
