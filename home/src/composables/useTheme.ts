import { ref, watch } from "vue";

const THEME_KEY = "nav-theme";

type ThemeMode = "light" | "dark" | "system";

const themeMode = ref<ThemeMode>((localStorage.getItem(THEME_KEY) as ThemeMode) || "system");

function getSystemDark(): boolean {
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function applyTheme() {
  const isDark = themeMode.value === "dark" || (themeMode.value === "system" && getSystemDark());
  document.documentElement.classList.toggle("dark", isDark);
}

// Listen for system theme changes
if (typeof window !== "undefined") {
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (themeMode.value === "system") {
      applyTheme();
    }
  });
}

// Apply on init
applyTheme();

watch(themeMode, (val) => {
  localStorage.setItem(THEME_KEY, val);
  applyTheme();
});

export function useTheme() {
  function toggleTheme() {
    const order: ThemeMode[] = ["light", "dark", "system"];
    const idx = order.indexOf(themeMode.value);
    themeMode.value = order[(idx + 1) % order.length];
  }

  function setTheme(mode: ThemeMode) {
    themeMode.value = mode;
  }

  const isDark = () =>
    themeMode.value === "dark" || (themeMode.value === "system" && getSystemDark());

  return {
    themeMode,
    toggleTheme,
    setTheme,
    isDark,
  };
}
