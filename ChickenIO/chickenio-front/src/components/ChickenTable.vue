<template>
  <div>
    <v-data-table style="cursor:pointer"
        :custom-filter="filterText"
        :headers="headers"
        :items="chickens"
        :search="search"
        class="elevation-1"
        item-key="name"
        @click:row="clickRow"
    >
      <template v-slot:top>
        <v-text-field
            v-model="search"
            class="mx-4"
            label="Search"
        ></v-text-field>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: "ChickenTable",
  data() {
    return {
      search: '',
      headers: [
        {
          text: 'Chicken Name',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        {text: 'RFID Tag', value: 'rfidTag'},
        {text: 'Birthdate', value: 'birthdate'},
        {text: 'Current Weight', value: 'weight'},
        {text: 'Current Daily Meal', value: 'meal'},
        {text: 'Some other column', value: 'someothervalue'},
      ],
      chickens: [
        {
          name: 'Gesicleide',
          rfidTag: 159,
          birthdate: 6.0,
          weight: 24,
          meal: 4.0,
          someothervalue: '1%',
        },
        {
          name: 'Ice cream sandwich',
          rfidTag: 237,
          birthdate: 9.0,
          weight: 37,
          meal: 4.3,
          someothervalue: '1%',
        },
        {
          name: 'Eclair',
          rfidTag: 262,
          birthdate: 16.0,
          weight: 23,
          meal: 6.0,
          someothervalue: '7%',
        },
        {
          name: 'Cupcake',
          rfidTag: 305,
          birthdate: 3.7,
          weight: 67,
          meal: 4.3,
          someothervalue: '8%',
        },
        {
          name: 'Gingerbread',
          rfidTag: 356,
          birthdate: 16.0,
          weight: 49,
          meal: 3.9,
          someothervalue: '16%',
        },
        {
          name: 'Jelly bean',
          rfidTag: 375,
          birthdate: 0.0,
          weight: 94,
          meal: 0.0,
          someothervalue: '0%',
        },
        {
          name: 'Lollipop',
          rfidTag: 392,
          birthdate: 0.2,
          weight: 98,
          meal: 0,
          someothervalue: '2%',
        },
        {
          name: 'Honeycomb',
          rfidTag: 408,
          birthdate: 3.2,
          weight: 87,
          meal: 6.5,
          someothervalue: '45%',
        },
        {
          name: 'Donut',
          rfidTag: 452,
          birthdate: 25.0,
          weight: 51,
          meal: 4.9,
          someothervalue: '22%',
        },
        {
          name: 'KitKat',
          rfidTag: 518,
          birthdate: 26.0,
          weight: 65,
          meal: 7,
          someothervalue: '6%',
        },
      ],
    }
  },
  methods: {
    filterText(value, search) {
      console.log(value)
      return value != null &&
          search != null &&
          typeof value === 'string' &&
          value.toString().toLocaleLowerCase().indexOf(search) !== -1
    },
    clickRow(value) {
      //insert click on row logic here
      console.log(value.name)
    }
  },
}
</script>

<style scoped>

</style>