import { ref } from 'vue';
import { defineStore } from 'pinia';
import { fetchSiteGet } from '@/service/api';

export const useSiteStore = defineStore('site', () => {
  const siteTitle = ref(localStorage.getItem('site_title') || '');

  async function fetchSiteTitle() {
    if (siteTitle.value) return siteTitle.value;
    try {
      const { data } = await fetchSiteGet();
      if (data?.title) {
        siteTitle.value = data.title;
        localStorage.setItem('site_title', data.title);
      }
    } catch {
      // ignore
    }
    return siteTitle.value;
  }

  return {
    siteTitle,
    fetchSiteTitle
  };
});
