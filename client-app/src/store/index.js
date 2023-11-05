import {createStore} from "vuex";

export default createStore({
    state: {
        user_info: {
            user_name: "admin",
            profile_photo: "src/assets/image/default-avatar.png",
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
            if(profile_photo.substring(0,3) === "/9j") {
                state.user_info.profile_photo = 'data:image/jpg;base64,' + profile_photo
            } else if(profile_photo.substring(0,3) === "iVB") {
                state.user_info.profile_photo = 'data:image/png;base64,' + profile_photo
            } else {
                state.user_info.profile_photo = "src/assets/image/default-avatar.png"
            }
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