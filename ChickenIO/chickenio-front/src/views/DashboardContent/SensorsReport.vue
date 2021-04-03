<template>
  <v-container fluid>
    <v-row justify-end>
      <v-col lg="6">
<!--        Remove height tags later-->
        <v-card height="600">
          <v-card-title>
            Video Stream
          </v-card-title>
          <v-card-subtitle>
            Insert video stream
          </v-card-subtitle>
        </v-card>
      </v-col>
      <v-col lg="6">
        <v-card height="300">
          <v-card-title>
            Temperature #1
          </v-card-title>
          <v-card-subtitle>
            Insert temperature chart here
          </v-card-subtitle>
        </v-card>
      </v-col>
      <v-col lg="6" >
        <v-card height="300">
          <v-card-title>
            Temperature #2
          </v-card-title>
          <v-card-subtitle>
            Insert temperature chart here
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "SensorsReport"
}
</script>

<style scoped>

</style>