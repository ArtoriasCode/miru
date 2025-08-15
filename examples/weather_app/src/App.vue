<template>
  <div class="content">
    <WeatherBlock/>
  </div>
</template>

<script>
import { miru } from '@/assets/js/miru'
window.miru = miru;
window.miru.setup();

import WeatherBlock from './components/WeatherBlock.vue'

export default {
  name: 'App',
  components: {
    WeatherBlock: WeatherBlock
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
