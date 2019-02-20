import Vue from 'vue'
import Router from 'vue-router'
import Chat from './views/Chat.vue'
import Login from './views/Login.vue'
import Axios from 'axios'

Vue.prototype.$http = Axios;

Vue.use(Router);

export default new Router({
  
  base: process.env.BASE_URL,
  routes: [
    { path: '/', name: 'chat', component: Chat},    
    { path: '/login', name: 'login', component: Login},
    { path: '/logout', name: 'logout'},
    { path: '*', redirect: '/'},
  ]
});