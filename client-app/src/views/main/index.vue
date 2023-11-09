<template>
  <img src="src/assets/image/inside_backpage1.jpg" class="background">
  <div class="secbackground"></div>
  <div class="main-container">
    <div>
      <el-tabs v-model="activeTab" @tab-change="change_tab" class="tabs">
        <!--- TODO -->
        <el-tab-pane label="主页" name="/main_page">
          <keep-alive>
            <div>here is main page</div>
          </keep-alive>
        </el-tab-pane>
        <el-tab-pane label="题目广场" name="/question_hub">
          <keep-alive>
            <question_hub v-if="activeTab === '/question_hub'"></question_hub>
          </keep-alive>
        </el-tab-pane>
        <el-tab-pane label="帖子广场" name="/post_hub">
          <keep-alive>
            <post_hub v-if="activeTab === '/post_hub'"></post_hub>
          </keep-alive>
        </el-tab-pane>
        <el-tab-pane label="用户群组" name="/team_hub">
          <keep-alive>
            <team_hub v-if="activeTab === '/team_hub'"></team_hub>
          </keep-alive>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="r-container">
      <el-button v-if="is_login" @click="logout" type="primary" :icon="SortDown" class="button">
        Logout
      </el-button>
      <el-button v-else @click="login" type="primary" :icon="SortUp" class="button">
        Login
      </el-button>
      <span v-if="!is_login" style="height:100%;">请先登录</span>
      <span v-else style="height:100%;">
        <el-button @click="change_tab('/user_center')" type="" text class="button1">
          <img :src="avatar" class="avatar">
          {{ user_name }},您好
        </el-button>
      </span>

    </div>
  </div>

</template>

<style scoped>
.tabs {
  position: fixed;
  top: 5%;
  left: 5%;
  right: 5%;
  bottom: 5%;
  width: 87%;
}

.main-container {
  top: 3%;
  left: 5%;
  width: 90%;
  height: 100vh;
}

.button1 {
  background-color: transparent;
}

.button {
  margin-right: 10px;
}

.r-container {
  position: fixed;
  top: 5%;
  right: 5%;
}

.secbackground {
  top: 3%;
  left: 2%;
  width: 96%;
  height: 100vh;
  position: fixed;
  z-index: 0;
  opacity: 90%;
  background-color: #f2f2f2;
}

.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 30%;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 5px;
}
</style>

<script>
import {SortDown, SortUp, User} from '@element-plus/icons-vue'
import {ref, watch} from "vue";
import router from "@/router";
import {userStateStore} from "@/store";
import Question_hub from "@/views/main/question_hub.vue";
import Post_hub from "@/views/main/post_hub.vue";
import Team_hub from "@/views/main/team_hub.vue";

export default {
  name: "index",
  components: {Team_hub, Post_hub, Question_hub},
  setup() {
    const store = userStateStore()
    const is_login = ref(store.getUserName);
    const tab_path = ref("/main_page");
    const avatar = ref(store.getProfilePhoto)
    const user_name = ref(store.getUserName)
    const activeTab = ref(sessionStorage.getItem('activeTab') || '/main_page')


    watch(activeTab, (newValue) => {
      sessionStorage.setItem('activeTab', newValue);
    });

    const change_tab = (name) => {
      tab_path.value = name;
    };

    const logout = () => {
      store.logout()
      router.push({path: '/log_reg'});
    };

    const login = () => {
      router.push({path: '/log_reg'});
    };

    return {
      activeTab,
      is_login,
      tab_path,
      change_tab,
      logout,
      login,
      avatar,
      user_name
    };
  },
  computed: {
    User() {
      return User;
    },
    SortUp() {
      return SortUp;
    },
    SortDown() {
      return SortDown;
    },
  },
}
</script>