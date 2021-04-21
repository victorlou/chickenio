<template>
  <v-navigation-drawer app class="orange lighten-1" dark permanent>
    <v-toolbar-title class="title"><img src="../../assets/hen.svg" class="logo" />ChickenIO</v-toolbar-title
    >
    <v-list>
      <v-list-item v-for="item in items" :key="item.title" :to="item.link" link>
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
          <v-btn class="white black--text" block> Logout </v-btn>
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
        { title: "Dashboard", icon: "mdi-view-dashboard", link: "/dashboard" },
        { title: "Galinhas", icon: "mdi-view-dashboard", link: "/reports" },
        { title: "Dados Ambientais", icon: "mdi-leak", link: "/sensors" },
        { title: "Sobre", icon: "mdi-help-box", link: "/about" },
      ],
      right: null,
      drawer: true,
    };
  },
};
</script>

<style scoped>
  .title {
    padding: 10px 20px;
    display: flex;
    align-items:center;
    color:#fff
  }
  .logo{
    width: 50px;
    margin-right: 30px;
  }
</style>