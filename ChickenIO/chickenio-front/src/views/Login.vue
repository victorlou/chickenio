<template>
  <v-main style="background-color: #E8BC5C">
    <v-container fill-height class="justify-center" >
      <LoginForm/>
    </v-container>
    <v-footer class="justify-center">
    Projeto desenvolvido para a disciplina de Oficina de Integração 3 - Equipe ChickenIO - 02/2020
    </v-footer>
  </v-main>
</template>

<script>
import LoginForm from "../components/LoginForm";

export default {
  name: "Login",
  components: {LoginForm}
}
</script>

<style scoped>

</style>