import {createStore} from "vuex";

export default createStore({
    state: {
        user_info: {
            username:'wwwzzzjjj',
            password:'123456',
            email:'xxx@xxx.com'
        }
    },
    getters: {

    },
    mutations: {
        setUserName(state, username) {
            state.user_info.username = username
        },
        setUserPassword(state, password) {
            state.user_info.password = password
        },
        setUserEmail(state, email) {
            state.user_info.email = email
        }
    }
})