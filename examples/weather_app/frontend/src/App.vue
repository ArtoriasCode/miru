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
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

#app {
  display: grid;
  place-items: center;
  padding: 20px;
  min-height: 100vh;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

html, body {
  margin: 0;
  padding: 0;
}

p, h1, h2, h3, h4, h5, h6 {
  margin: 0;
}

html {
  background-color: #eaeaea;
}

* {
  font-family: "Montserrat", sans-serif;
}
</style>
