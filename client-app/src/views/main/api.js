import axios from "axios";
import {ref} from "vue";

export function upload_ques_set(ques_set_data) {
    return axios.post('/upload_ques_set', ques_set_data,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        })
        .then(response => {
            return response.data
        })
}

export function update_team(team_data) {
    return axios.post('/update_team_info', team_data,
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
        data: JSON.stringify({})
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
            creator_name: creator_name,
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
            id: id,
            team_name: team_name,
            applier_name: applier_name,
            agree: agree
        })
    }).then(response => {
        return response.data
    })
}

export function del_ques_set(set_name) {
    return axios.request({
        url: '/del_ques_set',
        method: "post",
        data: JSON.stringify({
            ques_set_name: set_name,
        })
    }).then(response => {
        return response.data
    })
}

export function send_set_admin(uids, tid, current_user_id) {
    return axios.request({
        url: '/set_admin',
        method: "post",
        data: JSON.stringify({
            uids: uids,
            tid: tid,
            current_user_id: current_user_id
        })
    }).then(response => {
        return response.data
    })
}


export function check_team_perm(uid, tid) {
    return axios.request({
        url: '/is_team_admin',
        method: "post",
        data: JSON.stringify({
            tid:tid,
            uid:uid,
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_all_member(tid) {
    return axios.request({
        url: '/fetch_all_users_in_team',
        method: "post",
        data: JSON.stringify({
            tid: tid,
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_all_team_ques_set(tid) {
    return axios.request({
        url: 'fetch_all_ques_set_in_team',
        method: "post",
        data: JSON.stringify({
            tid: tid,
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_team_info(tid) {
    return axios.request({
        url: '/fetch_team_info',
        method: "post",
        data: JSON.stringify({
            tid: tid,
        })
    }).then(response => {
        return response.data
    })
}

export function change_password(uid,old_password,new_password) {
    return axios.request({
        url: '/change_password',
        method: "post",
        data: JSON.stringify({
            old_password:old_password,
            new_password:new_password,
            uid:uid
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_history_application(tid) {
    return axios.request({
        url: '/fetch_history_applications',
        method: "post",
        data: JSON.stringify({
            tid: tid,
        })
    }).then(response => {
        return response.data
    })
}

export function fetch_history_team(tid) {
    return axios.request({
        url: '/fetch_history_team',
        method: "post",
        data: JSON.stringify({
            tid: tid,
        })
    }).then(response => {
        return response.data
    })
}


export function del_members(del_user_ids, tid) {
    return axios.request({
        url: '/del_members',
        method: "post",
        data: JSON.stringify({
            del_user_ids: del_user_ids,
            tid: tid
        })
    }).then(response => {
        return response.data
    })
}

export function del_team(tid) {
    return axios.request({
        url: '/del_team',
        method: "post",
        data: JSON.stringify({
            tid: tid
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
            qs_id: form.qs_id,
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

export function hand_in_ans(form) {
    return axios.request(
        {
            url: '/judge_ans',
            method: "post",
            data: JSON.stringify(
                {
                    qids: form.qids,
                    types: form.types,
                    answers: form.answers,
                    standard_ans: form.standard_ans,
                    all_scores: form.all_scores
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function string2Array(string) {
    return string.match(/'([^']*)'/g).map(item => item.slice(1, -1))
}

export function array2String(array) {
    return "[" + array.map(item => "'" + item + "'").join(", ") + "]"
}

export function send_team_message(uids, tid, message) {
    return axios.request(
        {
            url: '/send_team_message',
            method: "post",
            data: JSON.stringify(
                {
                    uid_list: uids,
                    tid: tid,
                    message: message
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function fetch_favourite_sets(id) {
    return axios.request(
        {
            url: '/get_collections',
            method: "post",
            data: JSON.stringify(
                {
                    user_id: id,
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function hand_in_score(qids, scores, qsid, uid, answers) {
    return axios.request(
        {
            url: '/create_set_history',
            method: "post",
            data: JSON.stringify(
                {
                    qids: qids,
                    scores: scores,
                    qsid: qsid,
                    uid: uid,
                    answers: answers
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function create_exam(creator_id, start_time, duration, ques_set_name, exam_name) {
    return axios.request(
        {
            url: '/create_exam',
            method: "post",
            data: JSON.stringify(
                {
                    creator_id: creator_id,
                    start_time: start_time,
                    duration: duration,
                    ques_set_name: ques_set_name,
                    exam_name: exam_name
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function fetch_all_coming_test(uid) {
    return axios.request(
        {
            url: '/fetch_all_future_intime_tests',
            method: "post",
            data: JSON.stringify(
                {
                    uid: uid
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function check_inside_exam(uid, eid) {
    return axios.request(
        {
            url: '/inside_exam',
            method: "post",
            data: JSON.stringify(
                {
                    uid: uid,
                    eid: eid
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function participate_exam(uid, eid) {
    return axios.request(
        {
            url: '/participate_exam',
            method: "post",
            data: JSON.stringify(
                {
                    uid: uid,
                    eid: eid
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function fetch_exam_info(eid) {
    return axios.request(
        {
            url: '/fetch_exam_info',
            method: "post",
            data: JSON.stringify(
                {
                    eid: eid
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function fetch_set_history(uid) {
    return axios.request(
        {
            url: '/get_do_set_history',
            method: "post",
            data: JSON.stringify(
                {
                    uid: uid
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}

export function fetch_ques_history(uid, shid) {
    return axios.request(
        {
            url: '/get_do_ques_history',
            method: "post",
            data: JSON.stringify(
                {
                    uid: uid,
                    shid: shid
                }
            )
        }
    ).then(
        (response) => {
            return response.data
        }
    )
}
