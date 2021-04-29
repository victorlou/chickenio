import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import firebase from 'firebase'

Vue.use(VueAxios, axios)

Vue.config.productionTip = false

firebase.initializeApp({
  apiKey: "AIzaSyBxXAg-0Epn1C5VQYBGr8SC5WwIzdNqq7k",
  authDomain: "chicken-io.firebaseapp.com",
  projectId: "chicken-io",
  storageBucket: "chicken-io.appspot.com",
  messagingSenderId: "836973646165",
  appId: "1:836973646165:web:c8126c008b45a1f4b25fdc"
});

// Import CSS files (order is important)
import './assets/app.scss'

// Import Global Components
import GlobalComponents from './plugins/globalComponents.js'
Vue.use(GlobalComponents)

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
