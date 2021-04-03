<template>
  <div>
    <v-app-bar
        app
        color="orange lighten-1"
        dark
        dense
    >

      <v-toolbar-title>ChickenIO</v-toolbar-title>

      <v-spacer></v-spacer>

<!--      <v-btn icon>-->
<!--        <v-icon>mdi-heart</v-icon>-->
<!--      </v-btn>-->

<!--      <v-btn icon>-->
<!--        <v-icon>mdi-magnify</v-icon>-->
<!--      </v-btn>-->

<!--      <v-menu-->
<!--          bottom-->
<!--          left-->
<!--      >-->
<!--        <template v-slot:activator="{ on, attrs }">-->
<!--          <v-btn-->
<!--              v-bind="attrs"-->
<!--              v-on="on"-->
<!--              icon-->
<!--          >-->
<!--            <v-icon>mdi-dots-vertical</v-icon>-->
<!--          </v-btn>-->
<!--        </template>-->

<!--        <v-list>-->
<!--          <v-list-item-->
<!--              v-for="n in 5"-->
<!--              :key="n"-->
<!--              @click="() => {}"-->
<!--          >-->
<!--            <v-list-item-title>Option {{ n }}</v-list-item-title>-->
<!--          </v-list-item>-->
<!--        </v-list>-->
<!--      </v-menu>-->
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: "AppBar",
  data() {
    return {
      drawer: false
    }
  }
}
</script>

<style scoped>

</style>