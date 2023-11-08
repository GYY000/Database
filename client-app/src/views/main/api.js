import {ElMessage} from "element-plus";
import axios from "axios";

export function check_inside_group(data) {
    return axios.request({
        url: '/check_inside_group',
        method: "post",
        data: JSON.stringify({
            user_name: data.user_name,
            password: data.group_name,
        })
    }).then(
        (response) => {
            return response.data
        }
    ).catch(
        error => {
            ElMessage({
                message: '验证失败，请稍后再试',
                showClose: true,
                type: 'error',
            })
        }
    )
}

export function upload_ques_set(ques_set_data) {
    return axios.post('/upload_ques_set', ques_set_data,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        })
        .then(response => {
            return response.data
        })
}

export function fetch_all_visible_ques_set(user_id) {
    return axios.request({
        url: '/fetch_visible_ques_set',
        method: "post",
        data: JSON.stringify({
            user_id: user_id,
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_search_res(user_id, search_content) {
    return axios.request({
        url: '/search_visible_ques_set',
        method: "post",
        data: JSON.stringify({
            user_id: user_id,
            search_content: search_content.trim()
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_my_ques_sets(user_id) {
    return axios.request({
        url: '/fetch_create_ques_set',
        method: "post",
        data: JSON.stringify({
            user_id: user_id,
        })
    }).then(response => {
        return response.data
    })
}

export function upload_team(user_id) {
    return axios.request({
        url: '/upload_team',
        method: "post",
        data: JSON.stringify({
            user_id: user_id,
        })
    }).then(
        response => {
            return response.data
        }
    )
}
