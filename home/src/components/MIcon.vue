<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { isUrl } from "@/utils/window";
import { ref } from "vue";

defineOptions({
  name: "MIcon",
});
const props = defineProps({
  icon: {
    type: [String],
    default: "",
  },
  size: {
    type: [String, Number],
    default: 32,
  },
  color: {
    type: String,
    default: "",
  },
});

const imgLoaded = ref(false);
const imgError = ref(false);
const usedFallback = ref(false);

function handleImgLoad() {
  imgLoaded.value = true;
}

function handleImgError() {
  if (!usedFallback.value && props.icon) {
    // 尝试 Google Favicon fallback
    try {
      const url = new URL(props.icon);
      usedFallback.value = true;
      const img = document.querySelector<HTMLImageElement>(
        `img[data-icon-src="${props.icon}"]`,
      );
      if (img) {
        img.src = `https://www.google.com/s2/favicons?domain=${url.hostname}&sz=64`;
      }
    } catch {
      imgError.value = true;
    }
  } else {
    imgError.value = true;
  }
}

// 生成首字母
function getInitial(): string {
  if (!props.icon) return "?";
  try {
    const url = new URL(props.icon);
    return url.hostname.charAt(0).toUpperCase();
  } catch {
    return props.icon.charAt(0).toUpperCase();
  }
}
</script>

<template>
  <div class="flex items-center">
    <!-- URL 图标：带 fallback -->
    <template v-if="isUrl(<string>props.icon)">
      <!-- 加载失败后显示首字母占位 -->
      <div
        v-if="imgError"
        class="icon-fallback"
        :style="{
          width: `${size}px`,
          height: `${size}px`,
          backgroundColor: color || '#c0c4cc',
          fontSize: `${Number(size) * 0.45}px`,
        }"
      >
        {{ getInitial() }}
      </div>
      <!-- 正常图片 -->
      <img
        v-else
        :data-icon-src="icon"
        :width="`${size}px`"
        :height="`${size}px`"
        :src="icon"
        alt=""
        loading="lazy"
        :class="{ 'img-loaded': imgLoaded }"
        @load="handleImgLoad"
        @error="handleImgError"
      />
    </template>
    <!-- Iconify 图标 -->
    <icon v-else :icon="icon" v-bind="$attrs" :width="size" :height="size" :color="color || undefined" />
  </div>
</template>

<style lang="scss" scoped>
img {
  object-fit: fill;
  border-radius: 999px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

img.img-loaded {
  opacity: 1;
}

.icon-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  color: #fff;
  font-weight: 700;
  user-select: none;
  flex-shrink: 0;
}
</style>
