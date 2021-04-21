<template>
    <v-card class="main-card">
      <div class="justify-center card-title">
        <img src="../assets/hen.svg" class="logo">
        <h4>ChickenIO</h4>
      </div>
      <v-card-text>
        <div slot="card-content">
        <v-container>
          <v-row class="mt-0">
            <v-col cols="12">
              <v-text-field v-model="username" label="E-mail" :rules="nameRules" required></v-text-field>
            </v-col>
          </v-row>
          <v-row class="mt-0">
            <v-col cols="12">
              <v-text-field v-model="password" label="Senha" required></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col align="center">
              <v-btn class="btn-login" to="/dashboard" elevation="2" rased type="Submit">Entrar</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </div>
      </v-card-text>
    </v-card>
</template>

<script>
export default {
  name: "LoginForm",
  data: () => ({
    valid: false,
    username: '',
    password: '',
    nameRules: [
      v => !!v || 'Name is required',
      v => v.length <= 10 || 'Name must be less than 10 characters',
    ],
  }),
}
</script>

<style scoped>
  .main-card {
    padding: 35px;
    border-radius: 30px;
    width: 35vw;
    height: 45vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .card-title {
    background: #E8BC5C;
    position: absolute;
    padding: 15px;
    top: 0;
    border-bottom-left-radius: 40px;
    border-bottom-right-radius: 40px;
    border-top-left-radius: 0 !important;
    border-top-right-radius: 0 !important;
    color: #fff;
    font-size: 12px;
    width: 135px;
    height: 100px;
    justify-content: center;
    display: flex;
    align-items: center;
    flex-direction: column;
  }
  .logo {
    width: 40px
  }
  .btn-login {
    background-color: #E8BC5C !important;
    color: #fff !important
  }
</style>