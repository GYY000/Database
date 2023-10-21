import VueRouter from 'vue-router';
import user_login from "@/views/loginInterface/login";
import user_register from "@/views/loginInterface/register";

const routes = [
    {
        path: '/',
        name: "login-view",
        component: user_login,
    },
    {
        path: '/user-register',
        name: "register-view",
        component: user_register,
    }
]