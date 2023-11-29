<template>
  <img src="@/assets/image/inside_backpage1.jpg" class="background">
  <!--<div class="secbackground"></div>-->

  <el-menu :default-active="activeIndex" class="fixed-menu" mode="horizontal" @select="handleSelect">
    <img src="@/assets/image/logo.png" alt="Element logo" style="margin-left: 10px;margin-right: 10px;" />
    <el-menu-item index="/main_page">
      <el-icon>
        <House />
      </el-icon>
      首页
    </el-menu-item>
    <el-menu-item index="/question_hub">
      <el-icon>
        <Document />
      </el-icon>
      题目
    </el-menu-item>
    <el-menu-item index="/post_hub">
      <el-icon>
        <Postcard />
      </el-icon>
      帖子
    </el-menu-item>
    <el-menu-item index="/team_hub">
      <el-icon>
        <Avatar />
      </el-icon>
      团队
    </el-menu-item>

    <div class="r-container" style="position: absolute; right: 150px; top:20%">
      <el-badge :value="messages.id_list.length" v-if="messages !== null" :max="20" class="item" style="margin-right: 15px;" :hidden="messages.id_list.length === 0"> 
        <el-button plain
          v-if="is_login" @click="open_message_box" class="button">
          <el-icon>
            <Plus />
          </el-icon>
          申请
        </el-button>
      </el-badge>
      <el-button plain v-if="is_login" @click="() => { this.open_private_message = true }" :icon="Message"
        class="button">
        消息
      </el-button>

      <el-button plain v-if="is_login" @click="logout" :icon="SortDown" class="button">
        登出
      </el-button>
      <el-button plain v-else @click="login" :icon="SortUp" class="button">
        登录
      </el-button>
      <span v-if="!is_login">请先登录</span>
      <span v-else>
        <el-button @click="goto('/user_center')" type="" text class="button1">
          <img :src="avatar" class="avatar">
          {{ user_name }}
        </el-button>
      </span>
    </div>


  </el-menu>
  <div class="main-container">
    <keep-alive>
      <router-view name="main_page"></router-view>
    </keep-alive>
    <keep-alive>
      <router-view name="question_hub"></router-view>
    </keep-alive>
    <keep-alive>
      <router-view name="post_hub"></router-view>
    </keep-alive>
    <keep-alive>
      <router-view name="post_detail"></router-view>
    </keep-alive>
    <keep-alive>
      <router-view name="team_hub"></router-view>
    </keep-alive>


  </div>
  <el-dialog v-model="open_message" title="申请中心" center>
    <message_box :applier_name_list="messages.applier_name_list" :id_list="messages.id_list"
      :team_name_list="messages.team_name_list" :time_list="messages.time_list"></message_box>
  </el-dialog>
  <el-dialog v-model="open_private_message" title="私信" center style="width: 1000px;" @close="before_close_pm"
    @open="before_open_pm">
    <message_container ref="messageContainer"></message_container>
  </el-dialog>
</template>



<style scoped>
.fixed-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9999;
}

.tabs {
  position: fixed;
  top: 5%;
  left: 5%;
  right: 5%;
  bottom: 5%;
  width: 87%;
}

.main-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  height: 100vh;
  margin-top: 60px;
}

.button1 {
  background-color: transparent;
}

.button {
  width: 70px;
  border: 2px solid rgba(0, 0, 0, 0.342);

  display: flex;
  justify-content: center;
  align-items: center;
}

.r-container {
  display: flex;
  /* 使用 flex 布局 */
  align-items: center;
  /* 垂直居中 */
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
  width: 45px;
  height: 45px;
  border-radius: 50%;
  margin-right: 5px;
}
</style>

<script>
import { Message, SortDown, SortUp, User, Plus } from '@element-plus/icons-vue'
import { ref, watch } from "vue";
import router from "@/router";
import { userStateStore } from "@/store";
import Question_hub from "@/views/main/question_hub.vue";
import Post_hub from "@/views/main/post_hub.vue";
import Team_hub from "@/views/main/team_hub.vue";
import { fetch_all_application } from "@/views/main/api";
import Message_box from "@/views/main/message_box.vue";
import message_container from '@/views/main/site_message_component/message_container.vue';

export default {
  name: "index",
  components: { Message_box, Message, Team_hub, Post_hub, Question_hub, message_container },
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
    const activeIndex = ref("1")

    watch(activeTab, (newValue) => {
      sessionStorage.setItem('activeTab', newValue);
    });

    const change_tab = (name) => {
      tab_path.value = name;
      router.push({ path: tab_path.value })
    };

    const goto = (name) => {
      router.push({ path: name })
    };

    const logout = () => {
      store.logout()
      router.push({ path: '/log_reg' });
    };

    const login = () => {
      router.push({ path: '/log_reg' });
    };

    const open_message_box = () => {
      open_message.value = true
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
      open_private_message,
      activeIndex
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
  methods: {
    before_close_pm() {
      if (this.$refs.messageContainer.$refs.chatDisplay) {
        this.$refs.messageContainer.$refs.chatDisplay.stopTimer()
      }
    },
    before_open_pm() {
      if (this.$refs.messageContainer.$refs.chatDisplay) {
        this.$refs.messageContainer.$refs.chatDisplay.updateData()
      }
    },
    handleSelect(key) {
      this.activeIndex = key;
      console.log(key)
      this.$router.push(key);
    },
  },
}
</script>