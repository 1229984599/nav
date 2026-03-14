import { ref } from "vue";

const HISTORY_KEY = "search-history";
const MAX_HISTORY = 10;

function getHistory(): string[] {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
}

/**
 * Shared search utilities: history management + match priority sorting.
 */
export function useSearch() {
  const searchHistory = ref<string[]>(getHistory());

  function refreshHistory() {
    searchHistory.value = getHistory();
  }

  function addHistory(keyword: string) {
    if (!keyword.trim()) return;
    const history = getHistory().filter((h) => h !== keyword);
    history.unshift(keyword);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, MAX_HISTORY)));
    refreshHistory();
  }

  function removeHistory(keyword: string) {
    const history = getHistory().filter((h) => h !== keyword);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    refreshHistory();
  }

  function clearHistory() {
    localStorage.removeItem(HISTORY_KEY);
    refreshHistory();
  }

  /**
   * Sort links by match priority: title match > href match > desc match
   */
  function sortByMatchPriority<T extends { title?: string; href?: string }>(items: T[], q: string): T[] {
    const lower = q.toLowerCase();
    return [...items].sort((a, b) => {
      const pa = a.title?.toLowerCase().includes(lower) ? 0 : a.href?.toLowerCase().includes(lower) ? 1 : 2;
      const pb = b.title?.toLowerCase().includes(lower) ? 0 : b.href?.toLowerCase().includes(lower) ? 1 : 2;
      return pa - pb;
    });
  }

  return {
    searchHistory,
    getHistory,
    addHistory,
    removeHistory,
    clearHistory,
    sortByMatchPriority,
  };
}
