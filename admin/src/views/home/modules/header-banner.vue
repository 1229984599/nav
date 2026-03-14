<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useAppStore } from '@/store/modules/app';
import { useAuthStore } from '@/store/modules/auth';
import { $t } from '@/locales';
import { fetchSiteStats } from '@/service/api';

defineOptions({
  name: 'HeaderBanner'
});

const appStore = useAppStore();
const authStore = useAuthStore();

const gap = computed(() => (appStore.isMobile ? 0 : 16));

interface StatisticData {
  id: number;
  label: string;
  value: string;
}

const statisticData = ref<StatisticData[]>([
  { id: 0, label: '链接', value: '-' },
  { id: 1, label: '分类', value: '-' },
  { id: 2, label: '友链', value: '-' }
]);

onMounted(async () => {
  const { data, error } = await fetchSiteStats();
  if (!error && data) {
    statisticData.value = [
      { id: 0, label: '链接', value: String(data.link_count) },
      { id: 1, label: '分类', value: String(data.menu_count) },
      { id: 2, label: '友链', value: String(data.friend_count) }
    ];
  }
});
</script>

<template>
  <NCard :bordered="false" class="card-wrapper">
    <NGrid :x-gap="gap" :y-gap="16" responsive="screen" item-responsive>
      <NGi span="24 s:24 m:18">
        <div class="flex-y-center">
          <div class="size-72px shrink-0 overflow-hidden rd-1/2">
            <img src="@/assets/imgs/soybean.jpg" class="size-full" />
          </div>
          <div class="pl-12px">
            <h3 class="text-18px font-semibold">
              {{ $t('page.home.greeting', { userName: authStore.userInfo.userName }) }}
            </h3>
            <p class="text-#999 leading-30px">{{ $t('page.home.weatherDesc') }}</p>
          </div>
        </div>
      </NGi>
      <NGi span="24 s:24 m:6">
        <NSpace :size="24" justify="end">
          <NStatistic v-for="item in statisticData" :key="item.id" class="whitespace-nowrap" v-bind="item" />
        </NSpace>
      </NGi>
    </NGrid>
  </NCard>
</template>

<style scoped></style>
