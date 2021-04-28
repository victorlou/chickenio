<template>
  <v-container v-if="this.chartdata.datasets[0].data">
    <LineChart
      ref="chart"
      :chartdata="chartdata"
      :options="options"
    ></LineChart>
  </v-container>
</template>

<script>
import LineChart from "./LineChart.js";

export default {
  name: "FoodAmountChart",
  components: {
    LineChart,
  },
  props: {
    data: {
      type: Object,
    }
  },
  data() {
    return {
      chartdata: {
        labels: [],
        datasets: [
          {
            label: "Quantidade Programada (g)",
            data: null,
            backgroundColor: "transparent",
            borderColor: "rgba(63, 81, 181, 0.80)",
            pointBackgroundColor: "rgba(171, 71, 188, 1)",
            borderDash: [5, 5],
          },
          {
            label: "Quantidade ingerida (g)",
            data: null,
            backgroundColor: "transparent",
            borderColor: "rgba(75, 175, 80, 0.80)",
            pointBackgroundColor: "rgba(171, 71, 188, 1)",
          },
          {
            label: "Quantidade restante (g)",
            data: null,
            backgroundColor: "transparent",
            borderColor: "rgba(255, 0, 56, 0.60)",
            pointBackgroundColor: "rgba(171, 71, 188, 1)",
          },
        ],
      },
      options: {
        type: "line",
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: `Histórico de Comida Ingerida`,
        },
      },
    };
  },
  mounted() {
    this.updateData();
  },
  methods: {
    updateData() {
      this.chartdata.datasets[0].data = this.data.values.food_amount;
      this.chartdata.datasets[1].data = this.data.values.food_ate;
      this.chartdata.datasets[2].data = this.data.values.food_amount_at_end;
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