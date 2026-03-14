<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { createReusableTemplate } from '@vueuse/core';
import { useThemeStore } from '@/store/modules/theme';
import { fetchSiteStats } from '@/service/api';

defineOptions({
  name: 'CardData'
});

interface CardData {
  key: string;
  title: string;
  value: number;
  unit: string;
  color: {
    start: string;
    end: string;
  };
  icon: string;
}

const stats = ref({ link_count: 0, menu_count: 0, friend_count: 0, user_count: 0 });

const cardData = ref<CardData[]>([
  {
    key: 'linkCount',
    title: '链接总数',
    value: 0,
    unit: '',
    color: { start: '#ec4786', end: '#b955a4' },
    icon: 'pajamas:link'
  },
  {
    key: 'menuCount',
    title: '分类总数',
    value: 0,
    unit: '',
    color: { start: '#865ec0', end: '#5144b4' },
    icon: 'ep:menu'
  },
  {
    key: 'friendCount',
    title: '友链总数',
    value: 0,
    unit: '',
    color: { start: '#56cdf3', end: '#719de3' },
    icon: 'fluent-mdl2:message-friend-request'
  },
  {
    key: 'userCount',
    title: '用户总数',
    value: 0,
    unit: '',
    color: { start: '#fcbc25', end: '#f68057' },
    icon: 'mdi:user'
  }
]);

onMounted(async () => {
  const { data, error } = await fetchSiteStats();
  if (!error && data) {
    stats.value = data;
    cardData.value[0].value = data.link_count;
    cardData.value[1].value = data.menu_count;
    cardData.value[2].value = data.friend_count;
    cardData.value[3].value = data.user_count;
  }
});

interface GradientBgProps {
  gradientColor: string;
}

const [DefineGradientBg, GradientBg] = createReusableTemplate<GradientBgProps>();

const themeStore = useThemeStore();

function getGradientColor(color: CardData['color']) {
  return `linear-gradient(to bottom right, ${color.start}, ${color.end})`;
}
</script>

<template>
  <NCard :bordered="false" size="small" class="card-wrapper">
    <!-- define component start: GradientBg -->
    <DefineGradientBg v-slot="{ $slots, gradientColor }">
      <div
        class="px-16px pb-4px pt-8px text-white"
        :style="{ backgroundImage: gradientColor, borderRadius: themeStore.themeRadius + 'px' }"
      >
        <component :is="$slots.default" />
      </div>
    </DefineGradientBg>
    <!-- define component end: GradientBg -->

    <NGrid cols="s:1 m:2 l:4" responsive="screen" :x-gap="16" :y-gap="16">
      <NGi v-for="item in cardData" :key="item.key">
        <GradientBg :gradient-color="getGradientColor(item.color)" class="flex-1">
          <h3 class="text-16px">{{ item.title }}</h3>
          <div class="flex justify-between pt-12px">
            <SvgIcon :icon="item.icon" class="text-32px" />
            <CountTo
              :prefix="item.unit"
              :start-value="1"
              :end-value="item.value"
              class="text-30px text-white dark:text-dark"
            />
          </div>
        </GradientBg>
      </NGi>
    </NGrid>
  </NCard>
</template>

<style scoped></style>
