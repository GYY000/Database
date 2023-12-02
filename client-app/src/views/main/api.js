import axios from "axios";

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

export function fetch_all_application(user_id) {
    return axios.request({
        url: '/fetch_all_application',
        method: "post",
        data: JSON.stringify({
            user_id: user_id,
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_avatar(user_name) {
    return axios.request({
        url: '/get_profile_photo',
        method: "post",
        data: JSON.stringify({
            user_name: user_name,
        })
    }).then(response => {
        return response.data
    })
}

export function respond(id, team_name, applier_name, agree) {
    return axios.request({
        url: '/answer_to_req',
        method: "post",
        data: JSON.stringify({
            id:id,
            team_name:team_name,
            applier_name:applier_name,
            agree: agree
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_all_member(team_name) {
    return axios.request({
        url: '/fetch_all_users_in_team',
        method: "post",
        data: JSON.stringify({
            team_name:team_name,
        })
    }).then(response => {
        return response.data
    })
}

export function del_member(name, team_name) {
    return axios.request({
        url: '/del_member',
        method: "post",
        data: JSON.stringify({
            del_user_name: name,
            team_name: team_name
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_ques_info(qs_id) {
    return axios.request({
        url: '/fetch_all_ques',
        method: "post",
        data: JSON.stringify({
            qs_id: qs_id
        })
    }).then(response => {
        return response.data
    })
}

export function upload_picture(pic_form) {
    return axios.post('/editor_upload_pic', pic_form,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        }).then(
        response => {
            return response.data
        }
    )
}

export function upload_ques(form) {
    return axios.request({
        url: '/upload_ques',
        method: "post",
        data: JSON.stringify({
            ques_set_name: form.ques_set_name,
            content: form.content,
            serial_num: form.serial_number,
            score: form.score,
            creator_id: form.creator_id
        })
    }).then(response => {
        return response.data
    })
}

export function api_update_ques(form) {
    return axios.request(
        {
            url: 'update_ques',
            method: "post",
            data: JSON.stringify(
                {
                    is_delete: form.is_delete,
                    content: form.content,
                    qid: form.qid,
                    serial_num: form.serial_num,
                    score: form.score
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}