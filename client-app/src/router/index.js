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
            bar_show:true,
            header_show:true,
            footer_show:true
        }
    },
    {
        path: "/login",
        name: "login",
        component:user_login,
        meta: {
            bar_show:true,
            header_show:true,
            footer_show:true
        }
    },
    {
        path: '/register',
        name: "register",
        component: user_register,
        meta: {
            bar_show:true,
            header_show:true,
            footer_show:true
        }
    }
]


const router = createRouter({
    history: createWebHistory('/'),
    routes
})

router.beforeEach((to, from,next) =>{
    const isLogin = !!localStorage.eleToken && localStorage.getItem("isAuthentic") === "true"
    if (to.path === "/login") {
        // 若用户已登录且前往登录页，则跳转到首页
        isLogin ? next("/") : next()
    } else if (!(to.path === "/register") && !isLogin) { // 拦截
        next("/login")
    } else {
        next()
    }
})

export default router