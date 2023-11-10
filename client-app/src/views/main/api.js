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

export function fetch_all_teams() {
    return axios.request({
        url: '/fetch_all_teams',
        method: "post",
        data: JSON.stringify({
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

export function fetch_search_team_res(search_content) {
    return axios.request({
        url: '/search_team',
        method: "post",
        data: JSON.stringify({
            search_content: search_content.trim()
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_team_avatar(team_name) {
    return axios.request({
        url: '/fetch_team_avatar',
        method: "post",
        data: JSON.stringify({
            team_name: team_name.trim()
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_set_avatar(set_name) {
    return axios.request({
        url: '/fetch_set_avatar',
        method: "post",
        data: JSON.stringify({
            set_name: set_name.trim()
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

export function fetch_my_group(user_id) {
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

export function upload_team(team_data) {
    return axios.post('/upload_team', team_data,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        }).then(
        response => {
            return response.data
        }
    )
}

export function check_inside_group(user_id, group_name) {
    return axios.request({
        url: '/check_inside_group',
        method: "post",
        data: JSON.stringify({
            user_id: user_id,
            group_name: group_name,
        })
    }).then(response => {
        return response.data
    })
}

export function apply_for_team(creator_name, team_name, applier_id) {
    return axios.request({
        url: '/apply_for_team',
        method: "post",
        data: JSON.stringify({
            creator_name:creator_name,
            applier_id: applier_id,
            team_name: team_name,
        })
    }).then(response => {
        return response.data
    })
}
