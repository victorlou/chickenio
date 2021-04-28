<template>
  <v-container v-if="chartdata.datasets[0].data">
    <LineChart ref="chart" :chartdata="chartdata" :options="options"></LineChart>
  </v-container>
</template>

<script>
import LineChart from "./LineChart.js";

export default {
  name: "WeightHistoryChart",
  components: {
    LineChart,
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
            label: "Peso Médio (g)",
            data: null,
            backgroundColor: "transparent",
            borderColor: "rgba(1, 116, 188, 0.50)",
            pointBackgroundColor: "rgba(171, 71, 188, 1)",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          position: "top",
          text: [],
          fontSize: 14,
        },
      },
    };
  },
  mounted() {
    this.updateData();
  },
  methods: {
    updateData() {
      this.chartdata.datasets[0].data = this.data.values;
      this.chartdata.labels = this.data.timestamp;
      this.options.title.text[0] = `Peso Atual: ${this.data.currentWeight.weight.toFixed(
        1
      )} gramas`;
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