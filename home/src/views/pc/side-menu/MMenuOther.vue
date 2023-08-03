<script setup lang="ts">
import SubMenuItem from "./SubMenuItem.vue";

const items = [
  {
    title: "后台管理",
    icon: "simple-icons:phpmyadmin",
    color: "red",
    href: "/admin",
  },
];
</script>

<template>
  <div class="bg-white w-full z-10">
    <a
      class="p-4 w-full text-sm inline-block transform duration-300 hover:bg-[#f0f2f5]"
      :href="item.href"
      target="_blank"
      v-for="item in items"
    >
      <sub-menu-item :item="item" />
    </a>
  </div>
</template>

<style lang="scss" scoped></style>
