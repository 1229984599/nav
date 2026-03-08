<script setup lang="ts">
import { onMounted } from 'vue';
import { $t } from '@/locales';
import { useSiteStore } from '@/store/modules/site';

defineOptions({
  name: 'GlobalLogo'
});

interface Props {
  /** Whether to show the title */
  showTitle?: boolean;
}

withDefaults(defineProps<Props>(), {
  showTitle: true
});

const siteStore = useSiteStore();
onMounted(() => siteStore.fetchSiteTitle());
</script>

<template>
  <a href="/" class="w-full flex-center nowrap-hidden">
    <SystemLogo class="size-32px" />
    <h2 v-show="showTitle" class="pl-8px text-16px text-primary font-bold transition duration-300 ease-in-out">
      {{ siteStore.siteTitle || $t('system.title') }}
    </h2>
  </a>
</template>

<style scoped></style>
