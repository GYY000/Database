import {createStore} from "vuex";

export default createStore({
    state: {
        user_info: {
            username: undefined,
            profile_photo: undefined,
            register_date: undefined
        },
        isAuthentic: false
    },
    getters: {
    },
    mutations: {
        setUserName(state, username) {
            state.user_info.username = username
            localStorage.setItem("username", username)
        },
        setUserRegDate(state, date) {
            state.user_info.register_date = date
        },
        setUserProfilePhoto(state, profile_photo) {
            state.user_info.profile_photo = profile_photo
        },
        setAuthentic(state,authentic) {
          state.isAuthentic = authentic;
          localStorage.setItem("isAuthentic", authentic? "true":"false");
        }
    },
    actions: {
        async login_store_info({commit}, {accountInfo}) {
            commit("setUserName", accountInfo.username)
            commit("setUserRegDate", accountInfo.register_date)
            commit("setUserProfilePhoto", accountInfo.profile_photo)
            commit("setAuthentic", true)
        }
    }
})