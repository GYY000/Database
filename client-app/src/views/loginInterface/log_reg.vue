<template>
  <img src="/src/assets/image/background.jpg" class="background">
  <div class="position">
    <div class="container">
      <div class="tabs-container">
        <el-tabs v-model="activeName" :tab-position="'bottom'"
                 :stretch=true @tab-click="handleClick" class="tabs">
          <el-tab-pane name="sign-in" label="登录">
            <div class="title">
              Login
            </div>
          </el-tab-pane>
          <el-tab-pane name="register" label="注册">
            <div class="title">
              Register
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
      <div>
        <user_login v-if="isSignInMode"></user_login>
        <user_register v-else></user_register>
      </div>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import User_login from "@/views/loginInterface/login.vue";
import User_register from "@/views/loginInterface/register.vue";

export default {
  name: "log_reg",
  components: {User_login, User_register},
  setup() {
    const activeName = ref('sign-in')
    const isSignInMode = ref(true);
    const isRefresh = ref(true);
    const handleClick = (tab, event) => {
      isSignInMode.value = tab.index == 0;
      isRefresh.value = false
    };
    return {
      isSignInMode,
      handleClick,
      isRefresh,
      activeName
    };
  }
}
</script>

<style scoped>
.position {
  display: grid;
  justify-items: center;
  align-items: center;
  height: 100vh;
}

.container {
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, .25), 0 10px 10px rgba(0, 0, 0, .22);
  overflow: hidden;
  width: 400px;
  height: 400px;
  max-width: 100%;
  backdrop-filter: blur(2px);
  background: #f2f2f2;
  opacity: 95%;
}

.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
}

@font-face {
  font-family: 'Lobster';
  src: url('/src/assets/fonts/Lobster-1-4-1.otf') format('truetype');
}

.tabs {
  padding: 10px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.title {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Lobster', cursive;
  color: #409EFF;
  font-size: 50px;
  font-weight: 600;
}

.tabs-container {
  width: 100%;
}

el-tabs {
  min-width: 100%;
  display: flex;
}

el-tab-pane {
  flex: 1;
  text-align: center;
}
</style>