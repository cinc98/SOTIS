import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import AddTest from '../components/AddTest.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
    children: [{
      path: '/add-test',
      name: 'Add test',
      component: AddTest,
    }]
  },
  {
    path: '/',
    name: 'Login',
    component: Login
  },
]

const router = new VueRouter({
  routes
})

export default router
