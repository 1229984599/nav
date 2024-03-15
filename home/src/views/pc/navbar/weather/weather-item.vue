<script setup lang="ts">
import { computed, PropType } from "vue";
import { FutureWeatherType } from "@/api/spider";

defineOptions({
  name: "MWeatherItem",
});
const props = defineProps({
  item: {
    type: Object as PropType<FutureWeatherType>,
    required: true,
  },
  isNight: {
    type: Boolean,
    default: false,
  },
});

const icon_url = computed(() => {
  const icon = props.isNight
    ? `${props.item?.iconNight}n`
    : `${props.item?.iconDay}d`;
  return `https://cdn.qweather.com/img/plugin/190516/icon/c/${icon}.png`;
});
</script>

<template>
  <div class="weather-item">
    <span>{{ item.fxDate }}</span>
    <span>{{ item.tempMin }}°-{{ item.tempMax }}°</span>
    <img :src="icon_url" alt="" />
    <span>{{ isNight ? item.textNight : item.textDay }}</span>
  </div>
</template>

<style scoped lang="scss">
.weather-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2px 10px;
  color: white;
  font-size: 12px;

  & > span:first-child {
    font-size: 11px;
    font-weight: 700;
  }
  & > span:nth-child(2) {
    //color: #c49375;
  }

  & > img {
    max-width: 30px;
  }

  & > span:last-child {
    font-size: 12px;
    min-width: 2em;
    text-align: center;
  }
}
</style>
