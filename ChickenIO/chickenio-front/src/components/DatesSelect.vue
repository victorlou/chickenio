<template>
  <v-row>
    <v-col cols="12" lg="4">
      <v-menu
        ref="menuStartDate"
        v-model="menuStartDate"
        :close-on-content-click="false"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="startDateFormatted"
            label="Data Inicial"
            persistent-hint
            prepend-icon="mdi-calendar"
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="startDate"
          no-title
          @input="menuStartDate = false"
          locale="pt-br"
          :max="!endDate ? today : endDate"
        ></v-date-picker>
      </v-menu>
    </v-col>
    <v-col cols="12" lg="4">
      <v-menu
        ref="menuEndDate"
        v-model="menuEndDate"
        :close-on-content-click="false"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="endDateFormatted"
            label="Data Final"
            persistent-hint
            prepend-icon="mdi-calendar"
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="endDate"
          no-title
          @input="menuEndDate = false"
          locale="pt-br"
          :min="startDate"
          :max="today"
          :disabled="!startDate"
        ></v-date-picker>
      </v-menu>
    </v-col>
    <v-col>
      <v-radio-group v-model="periodType" row>
        <v-radio
          label="Média Diária"
          value="daily_avg"
          :disabled="startDate && endDate && startDate == endDate"
        ></v-radio>
        <v-radio label="Todas as medidas" value="all_data"></v-radio>
      </v-radio-group>
    </v-col>
  </v-row>
</template>

<script>
import moment from "moment";
export default {
  name: "DatesSelect",
  data() {
    return {
      startDate: null,
      endDate: null,
      periodType: "daily_avg",
      menuStartDate: false,
      menuEndDate: false,
    };
  },
  computed: {
    startDateFormatted() {
      return this.startDate && moment(this.startDate).format("DD/MM/YYYY");
    },
    endDateFormatted() {
      return this.endDate && moment(this.endDate).format("DD/MM/YYYY");
    },
    today() {
      return moment().format("YYYY-MM-DD");
    },
  },
  watch: {
    startDate() {
      if (this.startDate == this.endDate) {
        this.periodType = "all_data";
      }
      this.$emit("onChangeDate", this.startDate, 'startDate');
    },
    endDate() {
      if (this.startDate == this.endDate) {
        this.periodType = "all_data";
      }
      this.$emit("onChangeDate", this.endDate, 'endDate');
    },
    periodType() {
        this.$emit("onChangePeriodType", this.periodType);
    }
  },
};
</script>