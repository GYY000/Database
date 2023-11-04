import {createRouter, createWebHistory} from 'vue-router';
import user_login from "@/views/loginInterface/login.vue";
import user_register from "@/views/loginInterface/register.vue";
import index from "@/views/main/index.vue";
import main_page from "@/views/main/main_page.vue";
import user_center from "@/views/main/user_center.vue";
import store from "@/store";

const routes = [
    {
        path: '/',
        name: "index",
        component: index,
        meta: {
            bar_show: false,
            header_show: false,
            footer_show: false
        },
        children: [
            {
                path: '/main_page',
                name: "main_page",
                component: main_page,
                meta: {
                    bar_show: false,
                    header_show: false,
                    footer_show: false
                }
            },
            {
                path: '/user_center',
                name: "user_center",
                component: user_center,
                meta: {
                    bar_show: false,
                    header_show: false,
                    footer_show: false
                }
            }
        ]
    },
    {
        path: "/login",
        name: "login",
        component: user_login,
        meta: {
            bar_show: false,
            header_show: false,
            footer_show: false
        }
    },
    {
        path: '/register',
        name: "register",
        component: user_register,
        meta: {
            bar_show: false,
            header_show: false,
            footer_show: false
        }
    }
]


const router = createRouter({
    history: createWebHistory('/'),
    routes
})

router.beforeEach((to, from, next) => {
    const isLogin = store.getters.getIsAuthentic === true
    if (to.path === "/login") {
         //若用户已登录且前往登录页，则跳转到首页
        isLogin ? next("/") : next()
    } else if (!(to.path === "/register" || to.path === "/main_page") && !isLogin) { // 拦截
        next("/login")
    } else {
        next()
    }
})

export default router