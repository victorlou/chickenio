<template>
  <v-container>
    <v-row>
      <v-col cols="8">
        <v-text-field label="Chicken Name" type="text" required></v-text-field>
      </v-col>
      <v-col cols="4">
        <v-text-field label="RFID Tag" type="number" required></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <router-link to="/registerchicken">
      <v-col cols="12">
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