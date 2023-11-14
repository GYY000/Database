<template>
  <img src="@/assets/image/inside_backpage1.jpg" class="background">
  <div class="secbackground"></div>
  <div class="main-container">
    <div>
      <el-tabs v-model="activeTab" @tab-change="change_tab" class="tabs">
        <el-tab-pane label="主页" name="/main_page">
          <keep-alive>
            <router-view name="main_page"></router-view>
          </keep-alive>
        </el-tab-pane>
        <el-tab-pane label="题目广场" name="/question_hub">
          <keep-alive>
            <router-view name="question_hub"></router-view>
          </keep-alive>
        </el-tab-pane>
        <el-tab-pane label="帖子广场" name="/post_hub">
          <keep-alive>
            <router-view name="post_hub"></router-view>
          </keep-alive>
          <router-view name="post_detail"></router-view>
        </el-tab-pane>
        <el-tab-pane label="用户群组" name="/team_hub">
          <keep-alive>
            <router-view name="team_hub"></router-view>
          </keep-alive>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="r-container">
      <el-badge :value="messages.id_list.length" v-if="messages !== null" :max="20" class="item" style="margin-right: 30px;">
        <el-button v-if="is_login"
            @click="open_message_box" type="primary" :icon="Message" style="width:100%;"/>
      </el-badge>

      <el-button v-if="is_login"
        @click="()=>{this.open_private_message=true}" type="primary" :icon="Message" style="width:30px;"/>

      <el-button v-if="is_login" @click="logout" type="primary" :icon="SortDown" class="button">
        Logout
      </el-button>
      <el-button v-else @click="login" type="primary" :icon="SortUp" class="button">
        Login
      </el-button>
      <span v-if="!is_login" style="height:100%;">请先登录</span>
      <span v-else style="height:100%;">
        <el-button @click="goto('/user_center')" type="" text class="button1">
          <img :src="avatar" class="avatar">
          {{ user_name }},您好
        </el-button>
      </span>
    </div>
    <el-dialog v-model="open_message" title="申请中心" center>
      <message_box
          :applier_name_list="messages.applier_name_list"
          :id_list="messages.id_list"
          :team_name_list="messages.team_name_list"
          :time_list="messages.time_list"
      ></message_box>
    </el-dialog>

    <el-dialog v-model="open_private_message" title="私信" center>
      <message_container></message_container>
    </el-dialog>

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
  padding-right: 30px;
  width: 25%
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
import {Message, SortDown, SortUp, User} from '@element-plus/icons-vue'
import {ref, watch} from "vue";
import router from "@/router";
import {userStateStore} from "@/store";
import Question_hub from "@/views/main/question_hub.vue";
import Post_hub from "@/views/main/post_hub.vue";
import Team_hub from "@/views/main/team_hub.vue";
import {fetch_all_application} from "@/views/main/api";
import Message_box from "@/views/main/message_box.vue";
import message_container from '@/views/main/site_message_component/message_container.vue';

export default {
  name: "index",
  components: {Message_box, Message, Team_hub, Post_hub, Question_hub, message_container},
  setup() {
    const store = userStateStore()
    const is_login = ref(store.getIsAuthentic);
    const tab_path = ref("/main_page");
    const avatar = ref(store.getProfilePhoto)
    const user_name = ref(store.getUserName)
    const activeTab = ref(sessionStorage.getItem('activeTab') || '/main_page')
    const open_message = ref(false)
    const open_private_message = ref(false)
    const messages = ref(null)

    watch(activeTab, (newValue) => {
      sessionStorage.setItem('activeTab', newValue);
    });

    const change_tab = (name) => {
      tab_path.value = name;
      router.push({path: tab_path.value})
    };

    const goto = (name) => {
      router.push({path: name})
    };

    const logout = () => {
      store.logout()
      router.push({path: '/log_reg'});
    };

    const login = () => {
      router.push({path: '/log_reg'});
    };

    const open_message_box = () => {
      open_message.value=true
    }

    const init = () => {
      fetch_all_application(store.user_id).then(
          (response) => {
            messages.value = response
          }
      )
    }

    init()

    return {
      activeTab,
      is_login,
      tab_path,
      change_tab,
      logout,
      login,
      avatar,
      user_name,
      goto,
      open_message_box,
      open_message,
      messages,
      open_private_message
    };
  },

  computed: {
    Message() {
      return Message
    },
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