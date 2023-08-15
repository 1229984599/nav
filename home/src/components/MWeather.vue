<script setup>
window.WIDGET = {
  CONFIG: {
    modules: "01234",
    background: "5",
    tmpColor: "000000",
    tmpSize: "16",
    cityColor: "FF0000",
    citySize: "16",
    aqiColor: "FF9900",
    aqiSize: "16",
    weatherIconSize: "24",
    alertIconSize: "18",
    padding: "10px 10px 10px 10px",
    shadow: "0",
    language: "auto",
    fixed: "false",
    vertical: "top",
    horizontal: "left",
    key: "99ecd36cb84c4f3992227befc9c09c74",
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

<style lang="scss" scoped></style>
