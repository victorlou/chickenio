<template>
  <div>
    <NavDraw/>
    <AppBar/>
    <v-main>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>
  </div>
</template>

<script>

import AppBar from "@/components/Appbar/AppBar";
import NavDraw from "@/components/Appbar/NavDraw";

export default {
  name: "Dashboard",
  components: {NavDraw, AppBar},
}
</script>

<style lang="scss" scoped>
.wrapper {
  position: relative;
  top: 0;
  height: 100%;

  &.wrapper-full-page {
    min-height: 100vh;
    height: auto;
  }
}

.side-bar {
  position: relative;
  top: 0;
}

.main-panel {
  position: relative;
  float: right;

}
</style>