<template>
  <v-container fluid>
    <card
      Title="Cadastro de Galinhas"
      subTitle="Aqui você pode adicionar novas galinhas ao sistema"
    >
      <RegisterChickenForm slot="card-content"></RegisterChickenForm>
    </card>
  </v-container>
</template>

<script>
import RegisterChickenForm from "../../components/RegisterChickenForm";

export default {
  name: "RegisterChicken",
  components: { RegisterChickenForm },
};
</script>

<style scoped>
</style>