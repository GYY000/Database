<template>
  <head>
    <title>登录</title>
  </head>
  <body>
  <div>login</div>
  <div>
    <label>账号</label>
    <input v-model="username" placeholder="请输入您的账号">
  </div>
  <div>
    <label>密码</label>
    <input v-model="password" placeholder="请输入您的密码">
  </div>
  <button @click="submit">登录</button>
  <button @click="toRegister">注册</button>
  </body>
</template>

<style scoped>

</style>

<script>
import {fetch_user_info, user_login} from "@/views/loginInterface/loginAPI";
import {ElMessage} from "element-plus";

export default {
  name: "user_login",
  computed: {
    register() {
      return register
    }
  },

  data() {
    return {
      username: '',
      password: '',
      match: false,
    }
  },

  methods: {
    toRegister() {
      this.$router.push('/register')
    },
    submit() {
      const login_data = {
        "userName": this.userName,
        "password": this.password,
      }
      user_login(login_data).then(
          res => {
            this.match = res.match === "true"
          }
      ).then(
          () => {
            if (this.match) {
              fetch_user_info(this.username).then(
                  res => {
                    this.$store.dispatch("login_store_info", {accountInfo: res})
                    this.$router.push({path: '/'})
                  }
              )
            } else {
              ElMessage({
                message: 'login failed',
                type: 'error'
              })
            }
          }
      )
    }
  }
}
</script>