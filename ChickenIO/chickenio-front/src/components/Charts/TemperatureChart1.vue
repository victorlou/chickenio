<template>
  <v-container>
<!--    <LineChart v-if="loaded" :chartdata="chartdata" :options="options"></LineChart>-->
    <LineChart :chartdata="chartdata" :options="options"></LineChart>
  </v-container>
</template>

<script>
import LineChart from './LineChart.js'

export default {
  name: "Temperature",
  components: {
    LineChart
  },
  data() {
    return {
      chartdata: {
        labels: [
          "20/03/2020", "20/03/2020", "20/03/2020", "20/03/2020", "20/03/2020", "20/03/2020", "20/03/2020", "20/03/2020", "20/03/2020"
        ],
        datasets: [
          {
            label: "Weight",
            data: [2.8, 2.7, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.0, 3.0],
            backgroundColor: "transparent",
            borderColor: "rgba(1, 116, 188, 0.50)",
            pointBackgroundColor: "rgba(171, 71, 188, 1)"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: "Weight History"
        }
      }
    }
  },
  // async mounted() {
  //   this.loaded = false
  //   try {
  //     const {userlist} = await fetch('/api/userlist')
  //     this.chartdata = userlist
  //     this.loaded = true
  //   } catch (e) {
  //     console.error(e)
  //   }
  // }
}
</script>

<style scoped>

</style>