import { useWindowSize } from "@vueuse/core";
import { computed } from "vue";

const { width, height } = useWindowSize();

/**
 * 是否为移动端
 */
export const isMobile = computed(() => {
  return width.value < 768;
});

export const scrollTop = (selector: string) => {
  // document.documentElement.scrollTop = 0;
  const el = document.querySelector(selector) || window;
  el.scrollTo({
    top: 0,
    behavior: "smooth",
  });
};
