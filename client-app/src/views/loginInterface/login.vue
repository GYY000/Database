<template>
  <el-form
      label-position="left"
      label-width="100px"
      style="max-width: 300px;margin:auto">
    <el-form-item label="用户名">
      <el-input v-model="user_name"/>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="password" :show-password="true"/>
    </el-form-item>
  </el-form>
  <div class="centered">
    <el-button class="button" @click="submit">
      <div style="color:#409EFF">登 录</div>
    </el-button>
  </div>
</template>

<style scoped>
.centered {
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

<script>
import {ref} from "vue";
import {fetch_user_info, user_login} from "@/views/loginInterface/loginAPI";
import {ElMessage} from "element-plus";
import userStateStore from "@/store/index";
import router from "@/router";

export default {
  name: "user_login",
  setup() {
    const user_name = ref("");
    const password = ref("");
    const match = ref(false);

    const submit = () => {
      const login_data = {
        user_name: user_name.value,
        password: password.value,
      };
      const user = ref({
        user_name: '',
        password: '',
      });
      user_login(login_data)
          .then((res) => {
            match.value = Boolean(res.match === "true");
          })
          .then(() => {
            if (match.value) {
              fetch_user_info(user_name.value).then((res) => {
                const stateStore = userStateStore();
                stateStore.login_store_info(res);
                router.push({path: "/main_page"});
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
      submit,
    };
  },
};
</script>