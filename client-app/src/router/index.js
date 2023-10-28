import {createRouter, createWebHistory } from 'vue-router';
import user_login from "@/views/loginInterface/login.vue";
import user_register from "@/views/loginInterface/register.vue";

const routes = [
    {
        path: '/',
        name: "login-view",
        component: user_login,
    },
    {
        path: '/register',
        name: "register-view",
        component: user_register,
    }
]

const router = createRouter({
    history: createWebHistory('/'),
    routes
})

export default router