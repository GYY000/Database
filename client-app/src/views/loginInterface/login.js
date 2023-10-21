import {ElMessage} from "element-plus";
import axios from "axios"

export function user_login(login_data) {
    return axios.request()({url: '/loginInterface/login',
                                method: "post",
                                data: JSON.stringify({userName: login_data.userName,
                                    password: login_data.password})}).then(
        (response) => {
            return response.data
        }
    ).catch(
        msg => {
            ElMessage({
                message: '您输入的账号或密码不正确，请重新输入。',
                showClose: true,
                type: 'error',
            })
        }
    )
}
