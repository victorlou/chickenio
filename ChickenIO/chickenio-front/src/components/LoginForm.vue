<template>
    <v-card>
      <v-card-title primary-title class="justify-center">
        <h3>ChickenIO</h3>
      </v-card-title>
      <v-card-text>
        <div slot="card-content">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="username" label="User Name" :rules="nameRules" required></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="password" label="Password" required></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <router-link to="/dashboard">
            <v-col cols="12">
              <v-btn block elevation="2" rased type="Submit">Submit</v-btn>
            </v-col>
            </router-link>
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

</style>