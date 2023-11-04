import {createStore} from "vuex";

export default createStore({
    state: {
        user_info: {
            user_name: "admin",
            profile_photo: "default",
            register_date: "default"
        },
        isAuthentic: false
    },
    getters: {
        getUserName: state => state.user_info.user_name,
        getProfilePhoto: state => state.user_info.profile_photo,
        getRegisterDate: state => state.user_info.register_date,
        getIsAuthentic: state => state.isAuthentic
    },
    mutations: {
        setUserName(state, user_name) {
            state.user_info.user_name = user_name
            localStorage.setItem("user_name", user_name)
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
            commit("setUserName", accountInfo.user_name)
            commit("setUserRegDate", accountInfo.register_date)
            commit("setUserProfilePhoto", accountInfo.profile_photo)
            commit("setAuthentic", true)
        },
        async reg_success_info({commit}, {accountInfo}) {
            commit("setUserName", accountInfo.user_name)
            commit("setAuthentic", true)
        },
        async logout({commit}, {accountInfo}) {
            commit("setAuthentic", false)
        }
    }
})