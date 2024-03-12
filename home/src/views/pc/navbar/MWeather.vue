<script lang="js" setup>
import { useSiteStore } from "@/store/site";

const siteStore = useSiteStore();
window.WIDGET = {
  CONFIG: {
    modules: "01234",
    background: "5",
    tmpColor: "000000",
    tmpSize: "16",
    cityColor: "FF0000",
    citySize: "16",
    aqiColor: "FF9900",
    top: 0,
    aqiSize: "16",
    weatherIconSize: "24",
    alertIconSize: "18",
    padding: "10px 10px 10px 10px",
    shadow: "0",
    language: "auto",
    fixed: "false",
    vertical: "top",
    horizontal: "left",
    key: siteStore.siteInfo.weather_key,
  },
};
const script = document.createElement("script");
script.src =
  "https://widget.qweather.net/simple/static/js/he-simple-common.js?v=2.0";
document.body.appendChild(script);
</script>

<template>
  <div id="he-plugin-simple"></div>
</template>

<style lang="scss">
#he-plugin-simple {
  & > div > div {
    top: 45px !important;
  }
  & > a > div {
    &:last-child {
      width: unset !important;
    }
  }
}
#weather-view-he {
  height: auto !important;
}
</style>
