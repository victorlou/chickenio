<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" sm="6">
        <v-menu
          ref="menu"
          v-model="menu"
          :close-on-content-click="false"
          :return-value.sync="dates"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-combobox
              v-model="dates"
              multiple
              chips
              small-chips
              label="Intervalo"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-combobox>
          </template>
          <v-date-picker v-model="dates" multiple no-title scrollable locale="pt-br">
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="menu = false"> Cancelar </v-btn>
            <v-btn text color="primary" @click="changeDates()">
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </v-col>
    </v-row>
    <v-row justify-end>
      <v-col>
        <v-card>
          <v-card-title> Temperatura </v-card-title>
          <v-card-subtitle>
            <EnvironmentalChart
              type="temperature"
              title="Temperatura"
              color="rgba(255, 0, 56, 0.60)"
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
            />
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import EnvironmentalChart from "../../components/Charts/EnvironmentalChart";
export default {
  name: "SensorsReport",
  components: {
    EnvironmentalChart,
  },
  data() {
    return {
      dates: null,
      menu: false
    }
  },
  methods: {
    changeDates() {
      this.$refs.menu.save(this.dates)
      console.log(this.dates)
    }
  }
};
</script>

<style scoped>
</style>