<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { getPaletteColorByNumber, mixColor } from '@sa/color';
import { useAppStore } from '@/store/modules/app';
import { useThemeStore } from '@/store/modules/theme';
import { useSiteStore } from '@/store/modules/site';
import { $t } from '@/locales';
import PwdLogin from './modules/pwd-login.vue';

const appStore = useAppStore();
const themeStore = useThemeStore();
const siteStore = useSiteStore();

onMounted(() => siteStore.fetchSiteTitle());

const bgThemeColor = computed(() =>
  themeStore.darkMode ? getPaletteColorByNumber(themeStore.themeColor, 600) : themeStore.themeColor
);

const bgColor = computed(() => {
  const COLOR_WHITE = '#ffffff';
  const ratio = themeStore.darkMode ? 0.5 : 0.2;
  return mixColor(COLOR_WHITE, themeStore.themeColor, ratio);
});
</script>

<template>
  <div class="relative size-full flex-center overflow-hidden" :style="{ backgroundColor: bgColor }">
    <WaveBg :theme-color="bgThemeColor" />
    <NCard :bordered="false" class="relative z-4 w-auto rd-12px">
      <div class="w-400px lt-sm:w-300px">
        <header class="flex-y-center justify-between">
          <SystemLogo class="size-64px lt-sm:size-48px" />
          <h3 class="text-28px text-primary font-500 lt-sm:text-22px">{{ siteStore.siteTitle || $t('system.title') }}</h3>
          <div class="i-flex-col">
            <ThemeSchemaSwitch
              :theme-schema="themeStore.themeScheme"
              :show-tooltip="false"
              class="text-20px lt-sm:text-18px"
              @switch="themeStore.toggleThemeScheme"
            />
            <LangSwitch
              v-if="themeStore.header.multilingual.visible"
              :lang="appStore.locale"
              :lang-options="appStore.localeOptions"
              :show-tooltip="false"
              @change-lang="appStore.changeLocale"
            />
          </div>
        </header>
        <main class="pt-24px">
          <h3 class="text-18px text-primary font-medium">{{ $t('page.login.pwdLogin.title') }}</h3>
          <div class="pt-24px">
            <PwdLogin />
          </div>
        </main>
      </div>
    </NCard>
  </div>
</template>
