import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const about = () => import(/* webpackChunkName: "about" */ '../views/DashboardContent/About')
const login = () => import(/* webpackChunkName: "login" */ '../views/Login')
const Reports = () => import(/* webpackHuckName: "dashboard" */ '../views/DashboardContent/Reports')
const SensorsReport = () => import(/* webpackHuckName: "dashboard" */ '../views/DashboardContent/SensorsReport')
const RegisterChicken = () => import(/* webpackHuckName: "dashboard" */ '../views/DashboardContent/RegisterChicken')
const ChickenReport = () => import(/* webpackHuckName: "dashboard" */ '../views/DashboardContent/ChickenReport')
const Dashboard = () => import(/* webpackHuckName: "dashboard" */ '../views/Dashboard')

function verifyAuth(to, from, next) {
    const token = localStorage.getItem('token')
    if (!token) {
        next('/login')
    } else {
        next()
    }
}

const routes = [
    {
        path: '/',
        alias: ['/Home', '/index'],
        name: 'Home',
        component: Home,
        redirect: "/login",
        beforeEnter: verifyAuth
    },
    {
        path: '/login',
        name: 'Login',
        component: login
    },
    {
        path: "/dashboard",
        component: Dashboard,
        beforeEnter: verifyAuth,
        children: [
            {
                path: "/reports",
                name: "reports",
                component: Reports
            },
            {
                path: "/chickenreport/:tagCode",
                name: "chickenreport",
                component: ChickenReport
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
