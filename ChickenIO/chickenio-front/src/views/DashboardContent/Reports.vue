<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            <h4>Galinhas</h4>
          </v-card-title>
          <v-card-subtitle>
            <v-btn
              elevation="2"
              class="primary float-right mr-4"
              to="/registerchicken"
              type="button"
              >Adicionar nova</v-btn
            >
          </v-card-subtitle>
          <v-card-text>
            <ChickenTable @onSelectChicken="onSelectedChicken" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ChickenTable from "../../components/ChickenTable";

export default {
  name: "Charts",
  components: {
    ChickenTable,
  },
  data() {
    return {
      chicken: null,
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  methods: {
    onSelectedChicken(tagCode) {
      this.$router.push({ path: "/chickenreport/" + tagCode });
    },
  },
};
</script>

<style scoped>
</style>