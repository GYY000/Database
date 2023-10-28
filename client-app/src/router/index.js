import {createRouter, createWebHistory } from 'vue-router';
import user_login from "@/views/loginInterface/login.vue";
import user_register from "@/views/loginInterface/register.vue";
import index from"@/views/main/index.vue";

const routes = [
    {
        path: '/',
        name: "index",
        component: index,
        meta: {
            bar_show:true
        }
    },
    {
        path: "/login",
        name: "login",
        component:user_login,
    },
    {
        path: '/register',
        name: "register",
        component: user_register,
        meta: {
            bar_show: false
        }
    }
]


const router = createRouter({
    history: createWebHistory('/'),
    routes
})

router.beforeEach((to, from, next) => {

})

export default router