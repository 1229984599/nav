<script setup lang="ts">
import { onMounted } from 'vue';
import { useEcharts } from '@/hooks/common/echarts';
import { fetchSiteStats } from '@/service/api';

defineOptions({
  name: 'LineChart'
});

const { domRef, updateOptions } = useEcharts(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: [] as string[],
    axisLabel: {
      rotate: 30,
      fontSize: 11
    }
  },
  yAxis: {
    type: 'value',
    minInterval: 1
  },
  series: [
    {
      name: '链接数',
      type: 'bar',
      barWidth: '50%',
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: '#8e9dff' },
            { offset: 1, color: '#5da8ff' }
          ]
        }
      },
      data: [] as number[]
    }
  ]
}));

onMounted(async () => {
  const { data, error } = await fetchSiteStats();
  if (!error && data && data.distribution) {
    updateOptions(opts => {
      opts.xAxis.data = data.distribution.map(d => d.name);
      opts.series[0].data = data.distribution.map(d => d.value);
      return opts;
    });
  }
});
</script>

<template>
  <NCard :bordered="false" class="card-wrapper" title="分类链接统计">
    <div ref="domRef" class="h-360px overflow-hidden"></div>
  </NCard>
</template>

<style scoped></style>
