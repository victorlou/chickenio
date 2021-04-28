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
      <template v-slot:item.actions="{ item }">
        <v-icon color="red" @click.stop="openDialogDelete(item.id)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <v-row justify="space-around">
      <v-col cols="auto">
        <v-dialog
          v-model="dialog"
          transition="dialog-bottom-transition"
          max-width="600"
        >
          <v-card>
            <v-toolbar color="primary" dark>Remover Galinha</v-toolbar>
            <v-card-text>
              <div class="text-h5 pa-8">
                Deseja mesmo remover essa galinha do sistema?
              </div>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn text color="red" @click="dialog = false">Cancelar</v-btn>
              <v-btn text color="green" @click="deleteChicken()"
                >Confirmar</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
    <v-alert v-model="success" dense dismissible type="success">Galinha excluída com sucesso</v-alert>
    <v-alert v-model="error" dense dismissible type="error">Erro ao salvar dados da galinha</v-alert>
  </div>
</template>

<script>
import axiosClient from "../service/axiosClient";
import moment from "moment";

export default {
  name: "ChickenTable",
  data() {
    return {
      dialog: false,
      success: false,
      error: false,
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
        { text: "Ações", value: "actions", sortable: false },
      ],
      selectedChicken: null,
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
      return (
        value != null &&
        search != null &&
        typeof value === "string" &&
        value.toString().toLocaleLowerCase().indexOf(search) !== -1
      );
    },
    clickRow(value) {
      this.$emit("onSelectChicken", value.Tag.tag_code);
    },
    openDialogDelete(item) {
      this.dialog = true;
      this.selectedChicken = item;
      console.log(item);
    },
    deleteChicken() {
      axiosClient()
        .delete(`/chickens/delete/${this.selectedChicken}`)
        .then(() => {
          this.success = true;
          this.chickens = this.chickens.filter((el) => el.id !== this.selectedChicken)
        }).catch(() => {
          this.error = true;
        }).finally(() => this.dialog = false)
    },
  },
};
</script>

<style lang="scss">
.row-pointer > .v-data-table__wrapper > table > tbody > tr :hover {
  cursor: pointer;
}
</style>