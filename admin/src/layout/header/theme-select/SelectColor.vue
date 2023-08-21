<script lang="ts">
export default {
  name: "MSelectColor",
};
</script>
<template>
  <el-dialog
    title="提示"
    :model-value="isVisible"
    @close="handleCancel"
    width="22%"
  >
    <div class="center">
      <p class="title">切换主题</p>
      <el-color-picker
        v-model="mColor"
        :predefine="predefineColors"
      ></el-color-picker>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleConfirm">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { useVModel } from "@vueuse/core";
import { ref } from "vue";
import { useAppStore } from "@/store";

const props = defineProps<{
  modelValue: boolean;
}>();

const isVisible = useVModel(props, "modelValue");
const appStore = useAppStore();
// 预定义色值
const predefineColors = [
  "#ff4500",
  "#ff8c00",
  "#ffd700",
  "#90ee90",
  "#00ced1",
  "#1e90ff",
  "#c71585",
  "rgba(255, 69, 0, 0.68)",
  "rgb(255, 120, 0)",
  "hsv(51, 100, 98)",
  "hsva(120, 40, 94, 0.5)",
  "hsl(181, 100%, 37%)",
  "hsla(209, 100%, 56%, 0.73)",
  "#c7158577",
];
// 默认色值
const mColor = ref("#00ff00");

/**
 * 关闭
 */
function handleCancel() {
  isVisible.value = false;
}

function handleConfirm() {
  appStore.changeBgColor(mColor.value);
  handleCancel();
}
</script>

<style lang="scss" scoped>
.center {
  text-align: center;

  .title {
    margin-bottom: 12px;
  }
}
</style>
