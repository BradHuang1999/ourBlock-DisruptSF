import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import * as VueGoogleMaps from "vue2-google-maps";

Vue.use(VueMaterial);

Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyB6c0OGNGIHfcNplYRVIEZs3k8Mlkziv8Y"
  }
});

new Vue({
  render: h => h(App)
}).$mount('#app')
