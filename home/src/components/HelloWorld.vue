<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ msg: string }>()

const count = ref(0)
</script>

<template>
  <h1>{{ msg }}</h1>
  <h1 class="text-3xl font-bold underline">
    Hello world!
  </h1>
  <button class="btn btn-primary rounded-full">点我点我</button>

</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
