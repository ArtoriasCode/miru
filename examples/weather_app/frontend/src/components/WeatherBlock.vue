<template>
  <div class="block weather">
    <div class="current" v-if="forecast.length">
      <div class="temp">{{ selectedDay.temp }}°</div>
      <div class="condition">{{ selectedDay.condition }}</div>
      <div class="additional">
        <div class="wind">
          <svg class="icon">
            <use :href="windIcon + '#icon'"></use>
          </svg>
          <p>{{ selectedDay.wind }} mph</p>
        </div>
        <div class="humidity">
          <svg class="icon">
            <use :href="tearIcon + '#icon'"></use>
          </svg>
          <p>{{ selectedDay.humidity }}%</p>
        </div>
      </div>
    </div>
    <div class="forecast" v-if="forecast.length">
      <div class="days">
        <div
          v-for="(day, index) in forecast"
          :key="index"
          class="day"
          :class="{ active: day === selectedDay }"
          :data-wind="day.wind"
          :data-humidity="day.humidity"
          @click="selectDay(day)"
        >
          <p class="date">{{ day.date }}</p>
          <p class="temp">{{ day.temp }}°</p>
          <p class="condition">{{ day.condition }}</p>
        </div>
      </div>
    </div>
    <div class="search">
      <form @submit.prevent="fetchWeather">
        <input type="text" v-model="city" spellcheck="false" placeholder="Enter city" />
        <button type="submit">Search</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import windIcon from '@/assets/svg/wind.svg';
import tearIcon from '@/assets/svg/tear.svg';
import { ref } from 'vue';

const miru = window.miru;
const city = ref('');
const forecast = ref([]);

const selectedDay = ref(forecast.value[0]);

function selectDay(day) {
  selectedDay.value = day;
}

async function fetchWeather() {
  const data = await miru.call_py("get_weather_forecast", city.value);
  forecast.value = data;
  selectedDay.value = data[0];
}
</script>

<style lang="scss" scoped>
.content {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
}

.block {
  width: 100%;
  max-width: max-content;
  padding: 20px;
  border-radius: 26px;
  background-color: #fafafa;
}

.search {
  display: flex;
  align-items: center;
  justify-content: center;

  form {
    display: flex;
    gap: 10px;

    input {
      width: 100%;
      padding: 8px 12px;
      border: 1px solid #e8e8e8;
      color: #696969;
      border-radius: 8px;
      outline: none;
      font-weight: 500;
      font-size: 14px;
      font-family: "Montserrat", sans-serif;
    }

    button {
      padding: 8px 12px;
      background-color: #696969;
      border: none;
      border-radius: 8px;
      color: #fafafa;
      font-weight: 500;
      font-size: 14px;
      cursor: pointer;
    }
  }
}

.weather {
  box-sizing: border-box;

  .current {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    flex-direction: column;
    color: #696969;
    font-weight: 500;

    .temp {
      font-size: 200px;
      line-height: 1;
    }

    .condition {
      font-size: 40px;
      line-height: 1;
    }

    .additional {
      display: flex;
      gap: 20px;

      .wind, .humidity {
        display: flex;
        align-items: center;
        gap: 5px;

        svg {
          width: 100%;
          height: 100%;
          max-width: 25px;
          max-height: 25px;
        }
      }

      .humidity {
        svg {
          max-width: 22px;
        }
      }
    }
  }

  .forecast {
    margin-top: 40px;
    margin-bottom: 20px;

    .days {
      display: flex;
      gap: 20px;

      .day {
        display: flex;
        align-items: center;
        flex-direction: column;
        gap: 20px;
        padding: 20px;
        border: 2px solid transparent;
        border-radius: 20px;
        cursor: pointer;
        color: #696969;
        font-weight: 500;
        transition: .3s all;

        &:hover {
          border: 2px solid #e8e8e8;
        }

        &.active {
          border: 2px solid #e8e8e8;
        }

        .date {
          font-size: 16px;
          line-height: 1;
        }

        .temp {
          font-size: 28px;
          line-height: 1;
        }

        .condition {
          color: #a1a1a1;
          font-size: 16px;
          line-height: 1;
          max-width: 55px;
          overflow: hidden;
          white-space: nowrap;
          text-overflow: ellipsis;
        }
      }
    }
  }
}

@media (max-width: 1024px) {
  .weather {
    .forecast {
      .days {
        flex-wrap: wrap;
        justify-content: center;
      }
    }
  }
}

@media (max-width: 768px) {
  .weather {
    .current {
      .temp {
        font-size: 150px;
      }
    }
  }
}

@media (max-width: 480px) {
  .weather {
    .current {
      .temp {
        font-size: 120px;
      }
    }
  }
}
</style>
