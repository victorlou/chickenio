<template>
  <v-container fluid>
    <v-row justify-end>
      <v-col lg="6">
<!--        Remove height tags later-->
        <v-card height="600">
          <v-card-title>
            Video Stream
          </v-card-title>
          <v-card-subtitle>
            Insert video stream
          </v-card-subtitle>
        </v-card>
      </v-col>
      <v-col lg="6">
        <v-card height="300">
          <v-card-title>
            Temperature #1
          </v-card-title>
          <v-card-subtitle>
            <TemperatureChart1 />
          </v-card-subtitle>
        </v-card>
      </v-col>
      <v-col lg="6" >
        <v-card height="300">
          <v-card-title>
            Temperature #2
          </v-card-title>
          <v-card-subtitle>
            <TemperatureChart1 />
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import TemperatureChart1 from '../../components/Charts/TemperatureChart1'
// import TemperatureChart2 from "../../components/Charts/TemperatureChart2";
export default {
  name: "SensorsReport",
  components: {
    TemperatureChart1,
    // TemperatureChart2,
  }
}
</script>

<style scoped>

</style>