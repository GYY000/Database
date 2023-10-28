<template>
  <div class="container">
    <h1>用户注册</h1>
    <div>
      <label>用户名：</label>
      <input
        type="text"
        id="username"
        v-model="username"
      >
    </div>
    <div>
      <label>邮箱：</label>
      <input
        type="text"
        id="email_addr"
        v-model="email"
      >
    </div>
    <div>
      <label>密码：</label>
      <input
        type="text"
        id="password"
        v-model="password"
      >
    </div>
    <div>
      <label>请确认密码：</label>
      <input
        type="text"
        id="confirm_password"
        v-model="confirmPassword"
      >
    </div>
    <div>
      <button
        class="button"
        type="submit"
        @click="register"
      >
        注册
      </button>
    </div>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
import { user_register } from "@/views/loginInterface/loginAPI";

export default {
  name: "user_register",

  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
      email: "",
      can_reg: false
    };
  },

  methods: {
    register() {
      const register_data = {
        username: this.username,
        password: this.password,
        email: this.email
      };
      if (this.password === this.confirmPassword) {
        user_register(register_data).then(res => {
          this.can_reg = Boolean(res.is_successful === "false");
          if (res.duplicated === "true") {
            ElMessage.error("用户名已经被注册，请更换用户名");
          } else if (this.can_reg === false) {
            ElMessage.error("注册失败，请稍后再试");
          } else {
            ElMessage({
              message: "register successfully.",
              showClose: true,
              type: "success"
            });
            this.$router.push("/");
          }
        });
      } else {
        ElMessage.error("请确认密码一致");
      }
    }
  }
};
</script>

<style scoped>
.container {
  /* TODO: 添加样式 */
}

.button {
  /* TODO: 添加样式 */
}
</style>