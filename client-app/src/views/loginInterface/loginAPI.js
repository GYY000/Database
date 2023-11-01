import {ElMessage} from "element-plus";
import axios from "axios";

export function user_login(login_data) {
    return axios.request({
        url: '/loginInterface/login',
        method: "post",
        data: JSON.stringify({
            username: login_data.username,
            password: login_data.password
        })
    }).then(
        (response) => {
            return response.data
        }
    ).catch(
        error => {
            ElMessage({
                message: '登录失败，请稍后再试',
                showClose: true,
                type: 'error',
            })
        }
    )
}

export function fetch_user_info(login_user) {
    return axios.request(
        {
            url: '/loginInterface/fetch_info',
            method: "post",
            data: JSON.stringify({
                username: login_user
            })
        }).then(
        (response) => {
            return {
                username: login_user,
                register_date: response.data.register_date,
                profile_photo: response.data.profile_photo
            }
        }
    ).catch(
        error => {
            ElMessage({
                message: '无法获取用户信息',
                showClose: true,
                type: 'error',
            })
        }
    )
}

export function user_register(register_data) {
    return axios.request(
        {
            url: '/loginInterface/register',
            method: "post",
            data: JSON.stringify({
                username: register_data.username,
                password: register_data.password,
            })
        }).then(
        (response) => {
            return response.data;
        }
    ).catch(
        error => {
            ElMessage({
                message: '注册失败，请稍后再试',
                showClose: true,
                type: 'error',
            })
        }
    )
}
