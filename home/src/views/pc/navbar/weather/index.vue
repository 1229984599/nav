<script setup lang="ts">
import { FutureWeatherType, getWeather, WeatherType } from "@/api/spider";
import { computed, reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import MWeatherItem from "./weather-item.vue";

defineOptions({
  name: "MWeather",
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
  <div class="weather-container" v-show="weather?.temp">
    <span>{{ city }}</span>
    <span>{{ weather?.temp }}°C</span>
    <i :class="`qi-${weather?.icon}`"></i>
    <span>{{ weather?.text }}</span>
    <div class="weather-item-container">
      <m-weather-item
        :item="futureWeather"
        :key="index"
        v-for="(futureWeather, index) in futureWeatherList"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.weather-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  column-gap: 4px;
  margin-left: 10px;
  line-height: 45px;
  font-size: 13px;
  font-weight: 600;
  color: #c4652b;
  cursor: pointer;
  &:hover .weather-item-container {
    opacity: 1;
    visibility: visible;
    transform: translateY(0px);
  }
  & > i {
    padding: 0 2px;
    font-size: 18px;
  }

  & > .weather-item-container {
    position: absolute;
    //opacity: 1;
    //visibility: visible;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    transform: translateY(20px);
    left: 0;
    top: 100%;
    background-image: v-bind(bgUrl);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    min-width: 270px;
    line-height: 25px;
    //min-height: 300px;
    padding: 5px 8px;
    border-radius: 6px;
    // 在顶部露出一个三角形
    &:after {
      bottom: 100%;
      left: 25%;
      content: " ";
      height: 0;
      width: 0;
      position: absolute;
      pointer-events: none;
      border-color: rgba(255, 255, 255, 0);
      border-bottom-color: #27486e;
      border-width: 6px;
      margin-left: -6px;
    }
  }
}
</style>
