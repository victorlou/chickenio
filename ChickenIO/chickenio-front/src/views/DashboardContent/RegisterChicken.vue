<template>
  <v-container fluid>
    <card Title="Register Chicken" subTitle="Here you can register new chickens">
      <RegisterChickenForm slot="card-content"></RegisterChickenForm>
    </card>
  </v-container>
</template>

<script>
import RegisterChickenForm from '../../components/RegisterChickenForm';

export default {
  name: "RegisterChicken",
  components: {RegisterChickenForm},
  mounted() {
    console.log("mounted RegisterChickens")
  }
}
</script>

<style scoped>

</style>