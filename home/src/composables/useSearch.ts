import { computed, nextTick, ref, type Ref } from "vue";
import { useRouter } from "vue-router";
import linkModel from "@/api/links";
import { getBaiduSuggestions } from "@/api/spider";

const HISTORY_KEY = "search-history";
const MAX_HISTORY = 10;
const ENGINE_STORAGE_KEY = "search-engine";

// Search engines (shared single source of truth)
export const engines = [
  { key: "baidu", label: "百度", icon: "simple-icons:baidu", url: "https://www.baidu.com/s?wd=" },
  { key: "google", label: "Google", icon: "logos:google-icon", url: "https://www.google.com/search?q=" },
  { key: "bing", label: "Bing", icon: "logos:bing", url: "https://www.bing.com/search?q=" },
  { key: "github", label: "GitHub", icon: "mdi:github", url: "https://github.com/search?q=" },
] as const;

function getHistory(): string[] {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
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

/**
 * Shared search utilities: history, engines, suggestions.
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

  // Engine state (shared across components via same localStorage key)
  const activeEngine = ref(localStorage.getItem(ENGINE_STORAGE_KEY) || "baidu");
  const currentEngine = computed(() => engines.find((e) => e.key === activeEngine.value) || engines[0]);

  function setEngine(key: string) {
    activeEngine.value = key;
    localStorage.setItem(ENGINE_STORAGE_KEY, key);
  }

  // Autocomplete suggestion fetcher
  async function fetchSuggestions(
    queryString: string,
    callback: (arg: any) => void,
  ) {
    if (!queryString.trim()) {
      const history = getHistory();
      if (history.length) {
        return callback(
          history.map((h) => ({ title: h, _isHistory: true })),
        );
      }
      return callback([]);
    }
    const { items } = await linkModel.list(
      { page: 1, pageSize: 8, order_by: "order" },
      { keyword: queryString },
    );
    if (items.length === 0) {
      const baiduSuggestions = await getBaiduSuggestions(queryString);
      return callback(
        baiduSuggestions.map((s: any) => ({ ...s, _isExternal: true })),
      );
    }
    callback(sortByMatchPriority(items, queryString));
  }

  return {
    searchHistory,
    getHistory,
    addHistory,
    removeHistory,
    clearHistory,
    sortByMatchPriority,
    engines,
    activeEngine,
    currentEngine,
    setEngine,
    fetchSuggestions,
  };
}

/**
 * Shared search action handlers used by both MSearch and SearchDialog.
 *
 * @param searchQuery - reactive ref bound to the input
 * @param autocompleteRef - ref to the el-autocomplete instance
 * @param onComplete - cleanup callback after action (e.g. close dialog or clear input)
 */
export function useSearchActions(
  searchQuery: Ref<string>,
  autocompleteRef: Ref<any>,
  onComplete: () => void,
) {
  const router = useRouter();
  const { addHistory, removeHistory, currentEngine } = useSearch();

  function removeHistoryAndRefresh(keyword: string) {
    removeHistory(keyword);
    autocompleteRef.value?.close();
    nextTick(() => {
      autocompleteRef.value?.focus();
    });
  }

  function handleSuggestionClick(link: any) {
    if (link._isHistory) {
      searchQuery.value = link.title;
      handleEnterSearch();
      return;
    }
    if (!link.href) {
      handleExternalSearch(link.title);
      return;
    }
    addHistory(searchQuery.value || link.title);
    window.open(link.href, "_blank");
    onComplete();
  }

  function handleExternalSearch(kw: string = "") {
    const q = kw || searchQuery.value;
    if (!q) return;
    addHistory(q);
    window.open(currentEngine.value.url + encodeURIComponent(q), "_blank");
    onComplete();
  }

  function handleEnterSearch() {
    if (!searchQuery.value.trim()) return;
    addHistory(searchQuery.value);
    router.push({ path: "/search", query: { q: searchQuery.value } });
    onComplete();
  }

  return {
    removeHistoryAndRefresh,
    handleSuggestionClick,
    handleExternalSearch,
    handleEnterSearch,
  };
}
