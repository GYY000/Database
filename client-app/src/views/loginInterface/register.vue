<template>
  <el-form
      label-position="left"
      label-width="75px"
      style="max-width: 300px;margin:auto">
    <el-form-item label="用户名">
      <el-input v-model="user_name"/>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="password" :show-password="true"/>
    </el-form-item>
    <el-form-item label="确认密码">
      <el-input v-model="confirmPassword" :show-password="true"/>
    </el-form-item>
  </el-form>
  <div class="centered-button">
    <el-button @click="register" class="button">
      <div style="color:#409EFF">注 册</div>
    </el-button>
  </div>
</template>

<script>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { fetch_user_info, user_register } from "@/views/loginInterface/loginAPI";
import userStateStore from "@/store";
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
            const store = userStateStore();
            store.reg_success_info({ user_name: user_name.value })
            fetch_user_info(user_name.value).then((res) => {
              const store = userStateStore()
              store.login_store_info(res)
              router.push({ path: "/main_page" });
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
.centered-button {
    position: absolute;
    bottom: 20%;
    left: 50%;
    transform: translateX(-50%);
  }
.button {
  border-radius: 8px;
  height: 40px;
  width: 100px;
  border: 1px solid #409EFF;
}
</style>