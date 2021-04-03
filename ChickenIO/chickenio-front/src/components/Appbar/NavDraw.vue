<template>
  <v-navigation-drawer
      app
      class="orange lighten-1"
      dark
      permanent
  >
    <v-list>
      <v-list-item
          v-for="item in items"
          :key="item.title"
          :to="item.link"
          link
      >
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <router-link to="/login">
          <v-btn class="white black--text" block>
            Logout
          </v-btn>
        </router-link>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "NavDraw",
  data() {
    return {
      items: [
        {title: 'Chicken Report', icon: 'mdi-view-dashboard', link: '/reports'},
        {title: 'Sensors Report', icon: 'mdi-leak', link: '/sensors'},
        {title: 'Register Chicken', icon: 'mdi-image', link: '/registerchicken'},
        {title: 'About', icon: 'mdi-help-box', link: '/about'}
      ],
      right: null,
      drawer: true,
    }
  },
}
</script>

<style scoped>

</style>