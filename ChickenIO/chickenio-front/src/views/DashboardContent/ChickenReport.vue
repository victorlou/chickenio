<template>
  <v-container fluid>
    <v-row>
      <v-col lg="12" md="12" sm="12">
        <v-card>
          <v-card-title>
            <h4>Dados da Galinha</h4>
          </v-card-title>
          <v-card-text>
            <RegisterChickenForm
              :tagCode="tagCode"
              slot="card-content"
            ></RegisterChickenForm>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <DatesSelect
      @onChangeDate="changeDate"
      @onChangePeriodType="changePeriodType"
    />
    <v-row>
      <v-col lg="12" md="12" sm="12">
        <v-card>
          <v-card-title>
            <h4>Histórico de Peso</h4>
          </v-card-title>
          <v-card-text
            v-if="
              chartDataChickenWeight &&
              chartDataChickenWeight.timestamp.length > 0
            "
          >
            <WeightHistoryChart
              :data="chartDataChickenWeight"
            ></WeightHistoryChart>
          </v-card-text>
          <v-card-text v-else>
            <h3 style="text-align: center">
              Nenhum dado referente ao peso da galinha foi encontrado
            </h3>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-if="chicken && chicken.id">
        <v-card>
          <v-card-title>
            <h4>Histórico de Comida Ingerida</h4>
          </v-card-title>
          <v-card-text
            v-if="
              chartDataFoodAmount && chartDataFoodAmount.timestamp.length > 0
            "
          >
            <FoodAmountChart :data="chartDataFoodAmount" />
          </v-card-text>
          <v-card-text v-else>
            <h3 style="text-align: center">
              Nenhum dado referente ao a quantidade de comida ingerida da
              galinha foi encontrado
            </h3>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col lg="12" md="12" sm="12">
        <v-card>
          <v-card-title>
            <h4>Histórico de Ovos Botados</h4>
          </v-card-title>
          <v-card-text
            v-if="
              chartDataEggWeight &&
              chartDataEggWeight.timestamp.length > 0
            "
          >
            <EggHistoryChart
              :data="chartDataEggWeight"
            ></EggHistoryChart>
          </v-card-text>
          <v-card-text v-else>
            <h3 style="text-align: center">
              Nenhum dado referente aos ovos da galinha foi encontrado
            </h3>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import WeightHistoryChart from "../../components/Charts/WeightHistoryChart";
import EggHistoryChart from "../../components/Charts/EggHistoryChart";
import FoodAmountChart from "../../components/Charts/FoodAmountChart";
import RegisterChickenForm from "../../components/RegisterChickenForm";
import DatesSelect from "../../components/DatesSelect";
import axiosClient from "../../service/axiosClient";
import moment from "moment";

export default {
  name: "ChickenReport",
  components: {
    WeightHistoryChart,
    EggHistoryChart,
    RegisterChickenForm,
    FoodAmountChart,
    DatesSelect,
  },
  data() {
    return {
      chicken: {},
      tagCode: this.$route.params.tagCode,
      chartDataChickenWeight: null,
      chartDataFoodAmount: null,
      chartDataEggWeight: null,
      startDate: null,
      endDate: null,
      periodType: "daily_avg",
    };
  },
  mounted() {
    this.getChicken();
  },
  methods: {
    getChicken() {
      axiosClient()
        .get(`/chickens/${this.$route.params.tagCode}`)
        .then((response) => {
          this.chicken = response.data;
          this.chicken.birthdate = this.formatDate(this.chicken.birthdate);
          this.getData();
        });
    },
    async getChickenWeight() {
      try {
        const filter = `?start_date=${this.startDate}&end_date=${this.endDate}&period_type=${this.periodType}`;
        const { data } = await axiosClient().get(
          `${process.env.VUE_APP_API_BASE_URL}/chicken-weight-log/${this.chicken.id}${filter}`
        );
        this.chartDataChickenWeight = data;
      } catch (e) {
        console.log(e);
      }
    },
    async getFoodAmountChicken() {
      try {
        const filter = `?start_date=${this.startDate}&end_date=${this.endDate}&period_type=${this.periodType}`;
        const { data } = await axiosClient().get(
          `/feeder-weight-log/${this.chicken.id}${filter}`
        );
        this.chartDataFoodAmount = data;
      } catch (e) {
        console.error(e);
      }
    },
    async getEggHistory() {
      try {
        const filter = `?start_date=${this.startDate}&end_date=${this.endDate}&period_type=${this.periodType}`;
        const { data } = await axiosClient().get(
          `${process.env.VUE_APP_API_BASE_URL}/nest-weight-log/${this.chicken.id}${filter}`
        );
        this.chartDataEggWeight = data;
      } catch (e) {
        console.log(e);
      }
    },
    getData() {
      this.getChickenWeight();
      this.getFoodAmountChicken();
      this.getEggHistory()
    },
    formatDate(date) {
      return moment(date).format("DD/MM/YYYY");
    },
    changeDate(date, type) {
      if (type == "startDate") {
        this.startDate = date;
      } else if (type == "endDate") {
        this.endDate = date;
      }
      this.getData();
    },
    changePeriodType(periodType) {
      this.periodType = periodType;
      this.getData();
    },
  },
};
</script>

<style scoped>
</style>