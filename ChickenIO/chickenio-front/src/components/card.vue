<template>
    <v-card color="white" elevation="2" outlined :max-width="cardWidth">
      <v-card-title>
          <h4>{{ Title }}</h4>
      </v-card-title>
      <v-card-subtitle>
        <p>{{ subTitle }}</p>
      </v-card-subtitle>
      <v-card-text>
        <slot name="card-content"></slot>
      </v-card-text>
    </v-card>
</template>

<script>
export default {
  name: "card",
  props: {
    Title: {
      type: String,
      description: 'Card Title',
    },
    cardWidth: {
      type: Number,
      description: 'Max Width of Card',
  },
    subTitle: {
      type: String,
      description: 'Card Subtitle',
    }
  }
}
</script>

<style scoped>

</style>