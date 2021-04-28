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
            @click="!tagCode ? createChicken() : updateChicken()"
            >Salvar
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-alert v-model="success" dense dismissible type="success">Dados da galinha salvos com sucesso</v-alert>
          <v-alert v-model="error" dense dismissible type="error">Erro ao salvar dados da galinha</v-alert>
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
  props: {
    tagCode: {
      type: String,
    },
  },
  data() {
    return {
      success: false,
      error: false,
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
      chicken: {
        name: "",
      },
      tags: [],
    };
  },
  mounted() {
    this.getTags();
    if (this.tagCode) {
      this.getChickenData();
    }
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
    getChickenData() {
      axiosClient()
        .get(`/chickens/${this.$route.params.tagCode}`)
        .then((response) => {
          this.chicken = response.data;
          this.chicken.birthdate = this.formatDate(this.chicken.birthdate);
          this.tags.push(this.chicken.Tag);
        });
    },
    formatDate(date) {
      return moment(date).format("DD/MM/YYYY");
    },
    createChicken() {
      if (this.$refs.form.validate()) {
        axiosClient()
          .post(`/chickens/store`, {
            ...this.chicken,
            birthdate: this.formatDateToSql(this.chicken.birthdate),
          })
          .then(() => {
            this.success = true;
            this.updateTag();
          })
          .catch((e) => {
            this.error = true;
            console.log(e);
          });
      }
    },
    updateChicken() {
      if (this.$refs.form.validate()) {
        axiosClient()
          .put(`/chickens/edit/${this.chicken.id}`, {
            ...this.chicken,
            birthdate: this.formatDateToSql(this.chicken.birthdate),
          })
          .then(() => {
            this.success = true;
          })
          .catch((e) => {
            this.error = true;
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
        this.$router.push('/reports')
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