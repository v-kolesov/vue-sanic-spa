import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueNativeSock from 'vue-native-websocket'
import { getWebsocketUrl } from '@/utils'
Vue.config.productionTip = false


Vue.use(VueNativeSock, getWebsocketUrl(), {connectManually: true})

router.beforeEach((to, from, next) => {
  const isPublicUrl = to.name == 'login'      
  const token = localStorage.getItem('token')
  if (!isPublicUrl && !token) {                 
    next('/login')
  }
  next();
})

new Vue({
  router,  
  render: h => h(App)
}).$mount('#app')
