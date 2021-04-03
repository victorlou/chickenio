<template>
  <v-container>
    <LineChart :chartdata="chartdata" :options="options"></LineChart>
  </v-container>
</template>

<script>
import LineChart from './LineChart.js'

export default {
  name: "LineChartContainer",
  components: {
    LineChart
  },
  props: {
    chartdata: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
.small {
  max-width: 600px;
  margin: 150px auto;
}
</style>