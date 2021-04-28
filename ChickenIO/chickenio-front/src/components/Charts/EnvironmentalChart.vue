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
import axiosClient from "../../service/axiosClient";

export default {
  name: "EnvironmentalChart",
  components: {
    LineChart,
  },
  props: {
    type: {
      type: String,
    },
    title: {
      type: String,
    },
    color: {
      type: String,
    },
    startDate: {
      type: String,
    },
    endDate: {
      type: String,
    },
    periodType: {
      type: String,
    },
  },
  data() {
    return {
      chartdata: {
        labels: [],
        datasets: [
          {
            label: this.title,
            data: null,
            backgroundColor: "transparent",
            borderColor: this.color,
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
          text: `Histórico de ${this.title}`,
        },
      },
    };
  },
  watch: {
    startDate() {
      if (this.endDate) this.getData();
    },
    endDate() {
      if (this.startDate) this.getData();
    },
    periodType() {
      this.getData();
    },
  },
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      try {
        const filter = `?start_date=${this.startDate}&end_date=${this.endDate}&period_type=${this.periodType}`;
        const { data } = await axiosClient().get(
          `/environmental-log/${this.type}${filter}`
        );
        this.chartdata.datasets[0].data = data.values;
        this.chartdata.labels = data.timestamp;
        if (this.$refs.chart) {
          this.$refs.chart.renderChart(this.chartdata, this.options);
        }
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>

<style scoped>
</style>