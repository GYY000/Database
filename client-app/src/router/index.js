import {createRouter, createWebHistory} from 'vue-router';
import index from "@/views/main/index.vue";
import main_page from "@/views/main/main_page.vue";
import user_center from "@/views/main/user_center.vue";
import userStateStore from "@/store";
import log_reg from "@/views/loginInterface/log_reg.vue";
import question_hub from "@/views/main/question_hub.vue";
import post_hub from "@/views/main/post_hub.vue";
import team_hub from "@/views/main/team_hub.vue";

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
        path: "/log_reg",
        name: "log_reg",
        component: log_reg,
        meta: {
            bar_show: false,
            header_show: false,
            footer_show: false
        }
    },
]


const router = createRouter({
    history: createWebHistory('/'),
    routes
})

router.beforeEach((to, from, next) => {
    const store = userStateStore()
    const isLogin = store.getIsAuthentic
    if (to.path === "/log_reg") {
         //若用户已登录且前往登录页，则跳转到首页
        isLogin ? next("/") : next()
    } else if (to.path !== "/" && !isLogin) { // 拦截
        next("/log_reg")
    } else {
        next()
    }
})

export default router