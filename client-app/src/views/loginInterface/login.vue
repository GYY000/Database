<template>
  <div>
    <div>login</div>
    <div>
      <label>账号</label>
      <input v-model="user_name" placeholder="请输入您的账号" />
    </div>
    <div>
      <label>密码</label>
      <input v-model="password" placeholder="请输入您的密码" />
    </div>
    <button @click="submit">登录</button>
    <button @click="toRegister">注册</button>
  </div>
</template>

<style scoped></style>

<script>
import { ref } from "vue";
import { fetch_user_info, user_login } from "@/views/loginInterface/loginAPI";
import { ElMessage } from "element-plus";
import store from "@/store";
import router from "@/router";

export default {
  name: "user_login",

  setup() {
    const user_name = ref("");
    const password = ref("");
    const match = ref(false);

    const toRegister = () => {
      router.push("/register");
    };

    const submit = () => {
      const login_data = {
        user_name: user_name.value,
        password: password.value,
      };

      user_login(login_data)
        .then((res) => {
          match.value = Boolean(res.match === "true");
        })
        .then(() => {
          if (match.value) {
            fetch_user_info(user_name.value).then((res) => {
              store.dispatch("login_store_info", { accountInfo: res });
              router.push({ path: "/" });
            });
          } else {
            ElMessage({
              message: "login failed",
              type: "error",
            });
          }
        });
    };

    return {
      user_name,
      password,
      match,
      toRegister,
      submit,
    };
  },
};
</script>