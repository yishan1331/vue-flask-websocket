import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Monitor from '../views/Monitor.vue'
// import About_old from '../views/About_old.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/Monitor',
        name: 'Monitor',
        component: Monitor
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    // {
    //     path: '/About_old',
    //     name: 'About_old',
    //     component: About_old
    // },
]

const router = new VueRouter({
    routes
})

export default router
