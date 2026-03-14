<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { fetchSiteStats } from '@/service/api';

defineOptions({
  name: 'ProjectNews'
});

interface RecentLink {
  id: number;
  title: string;
  href: string;
  icon: string | null;
  create_time: string;
}

const recentLinks = ref<RecentLink[]>([]);

onMounted(async () => {
  const { data, error } = await fetchSiteStats();
  if (!error && data && data.recent_links) {
    recentLinks.value = data.recent_links;
  }
});

function openLink(href: string) {
  window.open(href, '_blank');
}
</script>

<template>
  <NCard title="最近添加" :bordered="false" size="small" segmented class="card-wrapper">
    <NList hoverable clickable>
      <NListItem v-for="item in recentLinks" :key="item.id" @click="openLink(item.href)">
        <template #prefix>
          <NAvatar v-if="item.icon" :src="item.icon" :size="36" round object-fit="contain" />
          <NAvatar v-else :size="36" round>
            {{ item.title.charAt(0) }}
          </NAvatar>
        </template>
        <NThing :title="item.title" :description="item.create_time" />
      </NListItem>
      <NEmpty v-if="recentLinks.length === 0" description="暂无链接" />
    </NList>
  </NCard>
</template>

<style scoped></style>
