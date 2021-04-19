<template>
  <div>
    <v-data-table
      :custom-filter="filterText"
      :headers="headers"
      :items="chickens"
      :search="search"
      class="elevation-1 row-pointer"
      item-key="id"
      @click:row="clickRow"
    >
      <template v-slot:top>
        <v-text-field
          v-model="search"
          class="mx-4"
          label="Pesquisar"
        ></v-text-field>
      </template>
      <template v-slot:item.birthdate="item">
        <span>{{ formatDate(item) }}</span>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import axiosClient from '../service/axiosClient';
import moment from "moment";

export default {
  name: "ChickenTable",
  data() {
    return {
      search: "",
      headers: [
        { text: "RFID Tag", value: "Tag.tag_code" },
        {
          text: "Nome",
          align: "start",
          sortable: false,
          value: "name",
        },
        {
          text: "Data de Nascimento",
          value: "birthdate",
        },
        // { text: "Peso Atual", value: "weight" },
        { text: "Número de refeições no dia", value: "meals_per_day" },
        { text: "Quantidade por refeição (g)", value: "food_quantity" },
      ],
      chickens: [],
    };
  },
  mounted() {
    this.getChickens();
  },
  methods: {
    getChickens() {
      axiosClient()
        .get(`${process.env.VUE_APP_API_BASE_URL}/chickens`)
        .then((response) => {
          this.chickens = response.data.chickens;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    formatDate(date) {
      return moment(date).format("DD/MM/YYYY");
    },
    filterText(value, search) {
      console.log(value);
      return (
        value != null &&
        search != null &&
        typeof value === "string" &&
        value.toString().toLocaleLowerCase().indexOf(search) !== -1
      );
    },
    clickRow(value) {
      //insert click on row logic here
      console.log("Clicked on table row"); // debug
      console.log(value); // debug
      this.$emit("onSelectChicken", value.id);
    },
  },
};
</script>

<style lang="scss">
.row-pointer > .v-data-table__wrapper > table > tbody > tr :hover {
  cursor: pointer;
}
</style>