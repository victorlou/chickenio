<template>
  <v-container v-if="chartdata.datasets[0].data">
    <BarChart ref="chart" :chartdata="chartdata" :options="options"></BarChart>
  </v-container>
</template>

<script>
import BarChart from "./BarChart.js";

export default {
  name: "EggHistoryChart",
  components: {
    BarChart,
  },
  props: {
    data: Object,
  },
  data() {
    return {
      chartdata: {
        labels: [],
        datasets: [
          {
            type: "line",
            label: "Peso dos ovos",
            data: null,
            backgroundColor: "transparent",
            borderColor: "rgba(1, 116, 188, 0.50)",
            pointBackgroundColor: "rgba(171, 71, 188, 1)",
            yAxisID: "y1",
            borderWidth: 3,
          },
          {
            type: "bar",
            label: "Quantidade de Ovos Botados",
            data: null,
            backgroundColor: "rgba(176, 16, 188, 0.50)",
            borderColor: "rgba(176, 16, 188, 0.50)",
            pointBackgroundColor: "rgba(171, 71, 188, 1)",
            // stepped: true,
            yAxisID: "y2",
            borderWidth: 3,
          },
        ],
      },
      options: {
        interaction: {
          mode: "index",
          intersect: false,
          axis: "x",
        },
        stacked: false,
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          position: "top",
          text: [],
          fontSize: 14,
        },
        scales: {
          yAxes: [
            {
              id: "y1",
              type: "linear",
              display: true,
              position: "left",
            },
            {
              id: "y2",
              type: "linear",
              display: true,
              position: "right",
              ticks: {
                stepSize: 1,
                beginAtZero: true,
              },
              grid: {
                drawOnChartArea: false,
              },
            },
          ],
        },
      },
    };
  },
  mounted() {
    this.updateData();
  },
  methods: {
    updateData() {
      this.chartdata.datasets[0].data = this.data.values.weight;
      this.chartdata.datasets[1].data = this.data.values.quantity;
      this.chartdata.labels = this.data.timestamp;
    },
  },
  watch: {
    data() {
      this.updateData();
      this.$refs.chart.renderChart(this.chartdata, this.options);
    },
  },
};
</script>

<style scoped>
</style>