<template>
  <div class="container">
    <h1>用户注册</h1>
    <div>
      <label>用户名：</label>
      <input type="text" id="user_name" v-model="user_name" />
    </div>
    <div>
      <label>密码：</label>
      <input type="text" id="password" v-model="password" />
    </div>
    <div>
      <label>请确认密码：</label>
      <input type="text" id="confirm_password" v-model="confirmPassword" />
    </div>
    <div>
      <button class="button" type="submit" @click="register">
        注册
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { fetch_user_info, user_register } from "@/views/loginInterface/loginAPI";
import store from "@/store";
import router from "@/router";

export default {
  name: "user_register",

  setup() {
    const user_name = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const can_reg = ref(false);

    const register = () => {
      const register_data = {
        user_name: user_name.value,
        password: password.value,
      };

      if (password.value === confirmPassword.value) {
        user_register(register_data).then((res) => {
          can_reg.value = Boolean(res.is_successful === "true");
          if (res.duplicated === "true") {
            ElMessage.error("用户名已经被注册，请更换用户名");
          } else if (!can_reg.value) {
            ElMessage.error("注册失败，请稍后再试");
          } else {
            ElMessage({
              message: "register successfully.",
              showClose: true,
              type: "success",
            });
            store.dispatch("reg_success_info", { accountInfo: { user_name: user_name.value } });
            fetch_user_info(user_name.value).then((res) => {
              store.dispatch("login_store_info", { accountInfo: res });
              router.push({ path: "/" });
            });
          }
        });
      } else {
        ElMessage.error("请确认密码一致");
      }
    };

    return {
      user_name,
      password,
      confirmPassword,
      can_reg,
      register,
    };
  },
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