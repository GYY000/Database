import {createRouter, createWebHistory} from 'vue-router';
import index from "@/views/main/index.vue";
import userStateStore from "@/store";
import log_reg from "@/views/loginInterface/log_reg.vue";
import user_center from "@/views/main/user_center.vue";

const routes = [
    {
        path: '/',
        name: "index",
        component: index,
        children: [
            {
                path: '/question_hub',
                name: "question_hub",
                components: {question_hub: () => import('@/views/main/question_hub.vue')}
            },
            {
                path: '/team_hub',
                name: "team_hub",
                components: {team_hub: () => import('@/views/main/team_hub.vue')},
            },
            {
                path: '/post_hub',
                name: "post_hub",
                components: {post_hub: () => import('@/views/main/post_hub.vue')}
            },
            {
                path: '/main_page',
                name: "main_page",
                components: {main_page: () => import('@/views/main/main_page.vue')}
            },
        ]
    },
    {
        path: "/log_reg",
        name: "log_reg",
        component: log_reg,
    },
    {
        path: '/user_center',
        name: "user_center",
        component: user_center
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
        isLogin ? next("/main_page") : next()
    } else if (to.path !== "/main_page" && !isLogin) { // 拦截
        next("/log_reg")
    } else {
        next()
    }
})

export default router