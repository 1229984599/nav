import { useWindowSize } from "@vueuse/core";
import { computed } from "vue";

const { width } = useWindowSize();

export const isMobile = computed(() => {
  return width.value < 960;
});
