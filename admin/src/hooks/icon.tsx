import { ref } from "vue";
import { CompositionColumns } from "@fast-crud/fast-crud/dist/d/d/crud";
import MIcon from "@/components/icon.vue";
import { isUrl } from "@/utils/window";
import { ElMessage } from "element-plus";

/**
 *
 * @param isShowValue 是否显示icon真实值
 * @param model api请求模型
 * @param isSyncIcon 是否需要同步到图床
 * @constructor
 */
export function UseIconForm(
  model: Object,
  isSyncIcon: boolean = false,
  isShowValue: boolean = false,
): CompositionColumns {
  const iconColor = ref("");
  const isLoading = ref(false);
  return {
    icon: {
      title: "图标",
      type: "text",
      column: {
        width: isShowValue ? 251 : 80,
        cellRender(scope) {
          return (
            <div class="flex items-center gap-x-2">
              <MIcon
                color={scope.row.color}
                icon={scope.value}
                size={30}
              ></MIcon>
              <div>
                {isShowValue ? <span>{scope.value}</span> : <span></span>}
              </div>
            </div>
          );
        },
        editable: { disabled: true },
      },
      form: {
        col: { span: 16 },
        helper: {
          render: () => {
            return (
              <a href="https://icon-sets.iconify.design/" target="_blank">
                点我前往iconify查看图标
              </a>
            );
          },
        },
        suffixRender(scope) {
          return (
            <div class="flex items-center ml-1 gap-x-1">
              {isSyncIcon ? (
                <el-button
                  disabled={!isUrl(scope.value)}
                  type="primary"
                  size="small"
                  icon="Refresh"
                  circle={true}
                  loading={isLoading.value}
                  onClick={() => {
                    isLoading.value = true;
                    model
                      .syncCdn(scope.value, scope.form.id)
                      .then((res: any) => {
                        scope.form.cdn_img_id = res.id;
                        scope.form.icon = res.url;
                        ElMessage.success("同步Cdn成功");
                      })
                      .finally(() => (isLoading.value = false));
                  }}
                ></el-button>
              ) : (
                ""
              )}
              <MIcon
                style={{ color: iconColor.value || scope.row.color }}
                icon={scope.value}
              ></MIcon>
            </div>
          );
        },
      },
    },
    color: {
      title: "颜色",
      type: "text",
      column: {
        show: false,
      },
      form: {
        col: { span: 4 },
        component: {
          name: "el-color-picker",
          props: {
            predefine: [
              "#ff4500",
              "#ff8c00",
              "#ffd700",
              "#90ee90",
              "#00ced1",
              "#1e90ff",
              "#c71585",
              "#c7158577",
            ],
          },
          onActiveChange(color: string) {
            iconColor.value = color;
          },
        },
      },
    },
    cdn_img_id: {
      title: "cdn图片id",
      type: "number",
      column: {
        show: false,
      },
      form: {
        show: false,
      },
    },
  };
}
