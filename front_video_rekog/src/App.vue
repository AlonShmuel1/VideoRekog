<script setup>
import VideoHandler from './components/VideoHandler.vue'
</script>

<template>
  <main>
    <VideoHandler />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

@media (min-width: 1024px) {
  header {
    padding-right: calc(var(--section-gap) / 2);
  }
}
</style>
