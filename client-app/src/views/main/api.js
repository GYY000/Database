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
    return axios.post('/upload_ques_set', formData,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        })
        .then(response => {
            console.log(response.data);
        })
}

export function user_register(register_data) {
    return axios.request(
        {
            url: '/loginInterface/register',
            method: "post",
            data: JSON.stringify({
                user_name: register_data.user_name,
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
