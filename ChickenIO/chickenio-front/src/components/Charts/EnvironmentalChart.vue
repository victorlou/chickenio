<template>
  <v-container v-if="this.chartdata.datasets[0].data">
    <LineChart :chartdata="chartdata" :options="options"></LineChart>
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
      type: String
    },
    title: {
      type: String
    },
    color: {
      type: String
    },
    dates: {
      type: Array
    }
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
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      try {
        const { data } = await axiosClient().get(
          `/environmental-log/${this.type}`
        );
        this.chartdata.datasets[0].data = data.avg;
        this.chartdata.labels = data.timestamp;
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>

<style scoped>
</style>