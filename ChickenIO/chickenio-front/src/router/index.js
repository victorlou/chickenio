import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const about = () => import(/* webpackChunkName: "about" */ '../views/DashboardContent/About')
const login = () => import(/* webpackChunkName: "login" */ '../views/Login')
const Reports = () => import(/* webpackHuckName: "dashboard" */ '../views/DashboardContent/Reports')
const SensorsReport = () => import(/* webpackHuckName: "dashboard" */ '../views/DashboardContent/SensorsReport')
const RegisterChicken = () => import(/* webpackHuckName: "dashboard" */ '../views/DashboardContent/RegisterChicken')
const Dashboard = () => import(/* webpackHuckName: "dashboard" */ '../views/Dashboard')

const routes = [
    {
        path: '/',
        alias: ['/Home', '/index'],
        name: 'Home',
        component: Home,
        redirect: "/login"
    },
    {
        path: '/login',
        name: 'Login',
        component: login
    },
    {
        path: "/dashboard",
        component: Dashboard,
        children: [

            {
                path: "/reports",
                name: "reports",
                component: Reports
            },
            {
                path: "/sensors",
                name: "sensors",
                component: SensorsReport
            },
            {
                path: "/registerchicken",
                name: "registerchicken",
                component: RegisterChicken
            },
            {
                path: '/about',
                name: 'About',
                component: about
            },
        ]
    },

]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
