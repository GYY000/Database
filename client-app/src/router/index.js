import {createRouter, createWebHistory} from 'vue-router';
import index from "@/views/main/index.vue";
import userStateStore from "@/store";
import log_reg from "@/views/loginInterface/log_reg.vue";
import user_center from "@/views/main/user_center.vue";
import do_problem from "@/views/quesDoing/do_problem.vue";
import edit_ques_group from "@/views/quesDoing/edit_ques_group.vue";
import post_detail from '@/views/main/post_detail.vue'
import main_page from "@/views/main/main_page.vue";
import post_hub from "@/views/main/post_hub.vue";
import team_hub from "@/views/main/team_hub.vue";
import question_hub from "@/views/main/question_hub.vue";
import panel_del_index from "@/views/main/panel_del_index.vue";
import manage_team from "@/views/main/team_component/manage_team.vue";

const routes = [
    {
        path: '/',
        name: "index",
        component: index,
        children: [
            {
                path: '/question_hub',
                name: "question_hub",
                component: question_hub
            },
            {
                path: '/team_hub',
                name: "team_hub",
                component: team_hub
            },
            {
                path: '/post_hub',
                name: "post_hub",
                component: post_hub
            },
            {
                path: '/main_page',
                name: "main_page",
                component: main_page
            },
            {
                path: '/post_detail/:pid',
                name: "post_detail",
                component: post_detail
            },
            {
                path: '/edit_ques_group/:qs_id',
                name: "edit_ques_group",
                component: edit_ques_group
            },
            {
                path: '/manage_team/:tid',
                name: "manage_team",
                component: manage_team
            }
        ]
    },
    {
        path: '/panel_del_index',
        name: "panel_del_index",
        component: panel_del_index,
        children: [
            {
                path: 'do_prob/:qs_id',
                name: "do_prob",
                component: do_problem
            }
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
    }
]


const router = createRouter({
    history: createWebHistory(),
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
    } else if (to.path === '/') {
        next("/main_page")
    } else {
        next()
    }
})

export default router