import { onBeforeUnmount, onMounted, ref } from "vue";

/**
 * Track scroll progress of .right-container element.
 * Returns scrollProgress (0–1) and scrollPercent (0–100).
 */
export function useScrollProgress(selector = ".right-container") {
  const scrollProgress = ref(0);
  const scrollPercent = ref(0);
  let _el: Element | null = null;

  function handleScroll() {
    if (!_el) return;
    const { scrollTop, scrollHeight, clientHeight } = _el as HTMLElement;
    if (scrollHeight <= clientHeight) {
      scrollProgress.value = 0;
      scrollPercent.value = 0;
    } else {
      const ratio = scrollTop / (scrollHeight - clientHeight);
      scrollProgress.value = ratio;
      scrollPercent.value = ratio * 100;
    }
  }

  onMounted(() => {
    // Defer to ensure DOM is rendered
    setTimeout(() => {
      _el = document.querySelector(selector);
      _el?.addEventListener("scroll", handleScroll, { passive: true });
    }, 100);
  });

  onBeforeUnmount(() => {
    _el?.removeEventListener("scroll", handleScroll);
    _el = null;
  });

  return { scrollProgress, scrollPercent };
}
