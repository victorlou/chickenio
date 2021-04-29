<template>
  <v-card class="main-card">
    <div class="justify-center card-title">
      <img src="../assets/hen.svg" class="logo" />
      <h4>ChickenIO</h4>
    </div>
    <v-card-text>
      <div slot="card-content">
        <v-container>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row class="mt-0">
              <v-col cols="12">
                <v-text-field
                  v-model="email"
                  label="E-mail"
                  :rules="emailRules"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="mt-0">
              <v-col cols="12">
                <v-text-field
                  v-model="password"
                  label="Senha"
                  :rules="passwordRules"
                  type="password"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-alert v-model="error" dense dismissible type="error">{{
              loginErrorMessage
            }}</v-alert>
            <v-row>
              <v-col align="center">
                <v-btn
                  class="btn-login"
                  @click="signIn()"
                  elevation="2"
                  rased
                  type="button"
                  >Entrar</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-container>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import axiosClient from "../service/axiosClient";
export default {
  name: "LoginForm",
  data: () => ({
    error: false,
    loginErrorMessage: "",
    valid: false,
    email: "",
    password: "",
    emailRules: [
      (v) => !!v || "E-mail é obrigatório",
      (v) => /.+@.+/.test(v) || "E-mail precisa ser válido",
    ],
    passwordRules: [(v) => !!v || "Senha é obrigatória"],
  }),
  methods: {
    signIn() {
      if (this.$refs.form.validate()) {
        axiosClient()
          .post("/user/login", { email: this.email, password: this.password })
          .then((response) => {
            localStorage.setItem("token", response.data.token);
            localStorage.setItem("user", JSON.stringify(response.data.user));
            this.$router.push("/reports");
          })
          .catch((e) => {
            localStorage.removeItem('token')
            this.error = true;
            this.loginErrorMessage = e.response.data.error;
          });
      }
    },
  },
};
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
  background: #e8bc5c;
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
  width: 40px;
}
.btn-login {
  background-color: #e8bc5c !important;
  color: #fff !important;
}
</style>