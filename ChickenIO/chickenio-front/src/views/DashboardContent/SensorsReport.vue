<template>
  <v-container fluid>
    <DatesSelect
      @onChangeDate="changeDate"
      @onChangePeriodType="changePeriodType"
    />
    <v-row justify-end>
      <v-col>
        <v-card>
          <v-card-title> Temperatura </v-card-title>
          <v-card-subtitle>
            <EnvironmentalChart
              type="temperature"
              title="Temperatura"
              color="rgba(255, 0, 56, 0.60)"
              :startDate="startDate"
              :endDate="endDate"
              :periodType="periodType"
            />
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify-end>
      <v-col lg="6">
        <v-card>
          <v-card-title> Umidade </v-card-title>
          <v-card-subtitle>
            <EnvironmentalChart
              type="air_humidity"
              title="Umidade"
              color="rgba(1, 116, 188, 0.50)"
              :startDate="startDate"
              :endDate="endDate"
              :periodType="periodType"
            />
          </v-card-subtitle>
        </v-card>
      </v-col>
      <v-col lg="6">
        <v-card>
          <v-card-title> Luminosidade </v-card-title>
          <v-card-subtitle>
            <EnvironmentalChart
              type="light"
              title="Luminosidade"
              color="rgba(188, 141, 1, 0.50)"
              :startDate="startDate"
              :endDate="endDate"
              :periodType="periodType"
            />
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import EnvironmentalChart from "../../components/Charts/EnvironmentalChart";
import DatesSelect from "../../components/DatesSelect";
export default {
  name: "SensorsReport",
  components: {
    EnvironmentalChart,
    DatesSelect,
  },
  data() {
    return {
      startDate: null,
      endDate: null,
      periodType: "daily_avg",
    };
  },
  methods: {
    changeDate(date, type) {
      if (type == "startDate") {
        this.startDate = date;
      } else if (type == "endDate") {
        this.endDate = date;
      }
    },
    changePeriodType(periodType) {
      this.periodType = periodType;
    },
  },
};
</script>

<style scoped>
</style>