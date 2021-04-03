<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-text-field label="Chicken Name" type="text" required></v-text-field>
      </v-col>
      <v-col>
        <v-text-field label="RFID Tag" type="number" required></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <router-link to="/registerchicken">
      <v-col>
        <v-btn block elevation="2" rased type="Submit">Submit</v-btn>
      </v-col>
      </router-link>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "RegisterChickenForm"
}
</script>

<style scoped>

</style>