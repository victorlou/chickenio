<template>
  <v-container fluid>
    <v-row>
      <v-col lg="6" md="6" sm="6">
        <v-card>
          <v-card-title>
            <h4>Name: {{ chicken.name }}</h4>
          </v-card-title>
          <v-img
              height="250"
              src="../../../public/biosecurity-chicken-in-mask.jpg"
          ></v-img>
        </v-card>
      </v-col>
      <v-col lg="6" md="6" sm="6">
        <v-card>
          <v-card-title>
            <h4>Information</h4>
          </v-card-title>
          <v-card-subtitle class="font-weight-bold">
            RFID: {{ chicken.rfidTag }} <br>
            Current weight: {{ chicken.currentWeight }} kg <br>
            Birthdate: {{ chicken.birthdate }} <br>
          </v-card-subtitle>
        </v-card>
      </v-col>
      <v-col lg="12" md="12" sm="12">
        <v-card>
          <v-card-title>
            <h4>Weight History</h4>
          </v-card-title>
          <v-card-subtitle>
            Weight history chart
          </v-card-subtitle>
          <v-card-text>
            <WeightHistoryChart></WeightHistoryChart>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import WeightHistoryChart from "../../components/Charts/WeightHistoryChart";

export default {
  name: "ChickenReport",
  components: {
    WeightHistoryChart
  },
  data() {
    return {
      chicken: {
        name: "Gesicleide",
        rfidTag: "123456789",
        birthdate: "01/04/2020",
        currentWeight: "3"
      },
      chickenReport: {
        averageFoodWeight: "300",
      },
      chartdata: {
        labels: ['January', 'February'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 20]
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  }
}
</script>

<style scoped>

</style>