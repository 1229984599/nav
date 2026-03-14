<script setup lang="ts">
import { onMounted } from 'vue';
import { useEcharts } from '@/hooks/common/echarts';
import { fetchSiteStats } from '@/service/api';

defineOptions({
  name: 'PieChart'
});

const { domRef, updateOptions } = useEcharts(() => ({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    bottom: '1%',
    left: 'center',
    itemStyle: {
      borderWidth: 0
    }
  },
  series: [
    {
      color: ['#5da8ff', '#8e9dff', '#fedc69', '#26deca', '#ec4786', '#56cdf3', '#f68057', '#865ec0'],
      name: '链接分布',
      type: 'pie',
      radius: ['45%', '75%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 1
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '12'
        }
      },
      labelLine: {
        show: false
      },
      data: [] as { name: string; value: number }[]
    }
  ]
}));

onMounted(async () => {
  const { data, error } = await fetchSiteStats();
  if (!error && data && data.distribution) {
    updateOptions(opts => {
      opts.series[0].data = data.distribution;
      return opts;
    });
  }
});
</script>

<template>
  <NCard :bordered="false" class="card-wrapper" title="分类链接分布">
    <div ref="domRef" class="h-360px overflow-hidden"></div>
  </NCard>
</template>

<style scoped></style>
