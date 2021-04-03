import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'

Vue.config.productionTip = false

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
