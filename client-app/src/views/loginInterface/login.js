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
                message: 'username and password do not match',
                showClose: true,
                type: 'error',
            })
        }
    )
}
