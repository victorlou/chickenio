<template>
  <v-container fluid>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-row>
        <v-col>
          <v-text-field
            label="Nome da Galinha"
            type="text"
            v-model="chicken.name"
            :rules="validate.name"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            label="Data de Nascimento"
            type="tel"
            v-mask="'##/##/####'"
            v-model="chicken.birthdate"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-select
            :items="tags"
            label="RFID Tag"
            v-model="chicken.tag_id"
            item-value="id"
            item-text="tag_code"
            :rules="validate.tag"
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            label="Número de refeições no dia"
            v-model="chicken.meals_per_day"
            type="tel"
            :rules="validate.meals_per_day"
            @blur="setDefaultInterval()"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            label="Quantidade por refeição (g)"
            v-model="chicken.food_quantity"
            type="tel"
            :rules="validate.food_quantity"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            label="Intervalo entre refeições (h)"
            v-model="chicken.meals_interval"
            type="tel"
            :rules="validate.meals_interval"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn
            class="success float-right"
            elevation="2"
            type="button"
            @click="createChicken()"
            >Cadastrar
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axiosClient from "../service/axiosClient";
import { mask } from "vue-the-mask";
import moment from "moment";

export default {
  name: "RegisterChickenForm",
  directives: { mask },
  data() {
    return {
      valid: false,
      validate: {
        name: [(v) => !!v || "Nome é obrigatório"],
        tag: [(v) => !!v || "Tag é obrigatório"],
        meals_per_day: [
          (v) => !!v || "Número de refeições no dia é obrigatório",
        ],
        food_quantity: [(v) => !!v || "Quantidade por refeição é obrigatório"],
        meals_interval: [
          (v) => !!v || "Intervalo entre refeições é obrigatório",
        ],
      },
      tags: [],
      chicken: {
        tag_id: "",
        food_quantity: "",
        meals_per_day: "",
        meals_interval: "",
      },
    };
  },
  mounted() {
    this.getTags();
  },
  methods: {
    getTags() {
      axiosClient()
        .get(`/available-tags`)
        .then((response) => {
          this.tags = response.data.tags;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    createChicken() {
      if (this.$refs.form.validate()) {
        axiosClient()
          .post(`/chickens/store`, {
            ...this.chicken,
            birthdate: this.formatDateToSql(this.chicken.birthdate),
          })
          .then(() => {
            this.updateTag();
          })
          .catch((e) => {
            console.log(e);
          });
      }
    },
    async updateTag() {
      const tag_code = this.tags.find((el) => el.id === this.chicken.tag_id)
        .tag_code;
      try {
        await axiosClient().put(`/tags/set-tag-status/${tag_code}`, {
          is_using: true,
        });
      } catch (e) {
        console.error(e);
      }
    },
    formatDateToSql(date) {
      return moment(date, "DD/MM/YYYY").format("YYYY-MM-DD");
    },
    setDefaultInterval() {
      switch (this.chicken.meals_per_day) {
        case "1":
          this.chicken.meals_interval = "0";
          break;
        case "2":
          this.chicken.meals_interval = 6;
          break;
        case "3":
          this.chicken.meals_interval = 3;
          break;
        case "4":
          this.chicken.meals_interval = 2;
          break;
        case "5":
          this.chicken.meals_interval = 1.5;
          break;
        default:
          this.chicken.meals_interval = 1;
      }
    },
  },
};
</script>

<style scoped>
</style>