<script setup lang="ts">
import { FutureWeatherType, getWeather, WeatherType } from "@/api/spider";
import { computed, reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import MWeatherItem from "./weather-item.vue";

defineOptions({
  name: "MWeather",
});

const props = defineProps({
  color: {
    type: String,
    default: "#c4652b",
  },
});

const city = ref("");
const weather = reactive<WeatherType>({});
const futureWeatherList = ref<FutureWeatherType[]>([]);
// 是否为晚上
const isNight = computed(() => {
  return new Date(String(weather.obsTime)).getHours() > 18;
});
// 动态获取背景图片
const bgUrl = computed(() => {
  const icon = isNight.value ? `${weather.icon}n` : `${weather.icon}d`;
  return `url(https://cdn.qweather.com/img/plugin/190516/bg/view/${icon}.png)`;
});

navigator.geolocation.getCurrentPosition(
  async ({ coords }) => {
    const location = `${coords.longitude},${coords.latitude}`;
    const data = await getWeather(location);
    city.value = data.city?.adm2;
    Object.assign(weather, data.weather);
    futureWeatherList.value = data.future_weather;
  },
  (positionError) => {
    switch (positionError.code) {
      case positionError.PERMISSION_DENIED:
        // 取消定位权限报错
        // ElMessage.error("定位权限失败，无法获取天气信息");
        break;
      case positionError.POSITION_UNAVAILABLE:
        ElMessage.error("定位失败");
        break;
      case positionError.TIMEOUT:
        ElMessage.error("定位超时");
        break;
      default:
        ElMessage.error("定位未知错误");
    }
  },
);
</script>

<template>
  <el-popover
    placement="bottom"
    :width="270"
    :offset="5"
    trigger="hover"
    :show-arrow="false"
    :popper-style="{
      backgroundImage: bgUrl,
      'background-size': 'cover',
      'background-position': 'center',
      border: 0,
    }"
  >
    <template #reference>
      <div class="weather-container" v-show="weather?.temp">
        <span>{{ city }}</span>
        <span>{{ weather?.temp }}°C</span>
        <i :class="`qi-${weather?.icon}`"></i>
        <span>{{ weather?.text }}</span>
      </div>
    </template>
    <template #default>
      <m-weather-item
        :item="futureWeather"
        :key="index"
        v-for="(futureWeather, index) in futureWeatherList"
      />
    </template>
  </el-popover>
</template>

<style scoped lang="scss">
.weather-container {
  display: flex;
  justify-content: center;
  align-items: center;
  column-gap: 4px;
  margin-left: 6px;
  //line-height: 45px;
  font-size: 13px;
  font-weight: 600;
  color: v-bind(color);
  cursor: pointer;
  @media screen and (min-width: 769px) {
    margin-left: 15px;
  }

  & > i {
    padding: 0 2px;
    font-size: 18px;
  }
}
</style>
