<template>
  <el-container style="height: 600px;">
    <el-container style="height: auto;">
      <el-aside :span="8">
        <h1>
          我的消息
        </h1>
        <el-input placeholder="请输入查找的用户" v-model="this.searched_username" @keyup.enter.native="search_user"> </el-input>
        <contact v-for="contact in contacts" :key="contact.user_id" :contact="contact" @open-message="handleContactClicked" />
        <div v-if="contacts.length == 0" style="display: flex; align-items: center; justify-content: center;"> 
          <svg v-if="loading_message == '加载中...'" version="1.1" id="loader-1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
            width="30px" height="30px" viewBox="0 0 40 40" enable-background="new 0 0 40 40" xml:space="preserve">
            <path opacity="0.2" fill="#000" d="M20.201,5.169c-8.254,0-14.946,6.692-14.946,14.946c0,8.255,6.692,14.946,14.946,14.946
              s14.946-6.691,14.946-14.946C35.146,11.861,28.455,5.169,20.201,5.169z M20.201,31.749c-6.425,0-11.634-5.208-11.634-11.634
              c0-6.425,5.209-11.634,11.634-11.634c6.425,0,11.633,5.209,11.633,11.634C31.834,26.541,26.626,31.749,20.201,31.749z"/>
            <path fill="#000" d="M26.013,10.047l1.654-2.866c-2.198-1.272-4.743-2.012-7.466-2.012h0v3.312h0
              C22.32,8.481,24.301,9.057,26.013,10.047z">
              <animateTransform attributeType="xml"
                attributeName="transform"
                type="rotate"
                from="0 20 20"
                to="360 20 20"
                dur="0.5s"
                repeatCount="indefinite"/>
            </path>
          </svg>
          <span> {{ loading_message }}  </span>
        </div>
      </el-aside>
      <el-container>
        <el-header style="background-color:#DDE4F2;">
          <p style="font-size: 20px; margin-top: 0;">
            {{ cur_contact.user_name }}
          </p>
        </el-header>
        <el-main style="padding-right: 0; padding-top: 0; padding-bottom: 0;">
          <chat_display v-if="Object.keys(cur_contact).length > 0" :contact="cur_contact" ref="chatDisplay"></chat_display>
          <div v-else>暂无</div>
        </el-main>
        <el-footer style="display: flex; align-items: center;">
          <el-input placeholder="请输入内容" v-model="this.new_message" @keyup.enter.native="send"> </el-input>
          <el-button type="success" @click="send">发送</el-button>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>
  
<script>
import contact from "@/views/main/site_message_component/contact.vue";
import chat_display from "@/views/main/site_message_component/chat_display.vue";
import axios from 'axios';
import userStateStore from "@/store";
export default {
  name: "message_container",
  components: {
    contact,
    chat_display
  },
  data() {
    return {
      contacts: [
      ],
      cur_contact: {},
      new_message: '',
      searched_username: '',
      loading_message: '加载中...'
    };
  },
  mounted () {
    this.fetchAllContact()
  },
  beforeDestroy() {
    console.log(destroyed)
  },
  methods: {
    handleContactClicked(contact) {
      // 处理点击联系人的逻辑
      this.cur_contact = contact
      console.log("点击的联系人:", contact);
    },
    fetchAllContact() {
      const store = userStateStore()
      const request = {
        uid: store.getUserId
      }
      axios.post("/get_all_relative_person", request)
        .then(response => {
          this.contacts = response.data
          if (this.contacts.length == 0) {
            this.loading_message = '还没有人给你发消息哦';
          }
        })
        .catch(error => {
          console.error(error);
      });
    },
    send() {
      const store = userStateStore()
      axios.post('/send_message', { sender_id: store.getUserId, receiver_name: this.cur_contact.user_name, content: this.new_message})
        .then(response => {
          this.new_message = ''
          //this.messages.push(response.data)
        })
        .catch(error => {
          console.error(error);
        });
    },
    search_user() {
      let contact = this.contacts.find(contact => contact.user_name === this.searched_username)
      if (contact) {
        this.cur_contact = contact
        return
      }
      axios.post('/search_user', { user_name: this.searched_username })
        .then(response => {
          if (response.data.has_user) {
            let new_contact = {user_name: this.searched_username, user_id: response.data.uid, has_unread_message: false}
            this.contacts.unshift(new_contact)
            this.searched_username = ''
            this.cur_contact = new_contact
          } else {
            alert("找不到用户" + this.searched_username)
          }
          //this.messages.push(response.data)
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>
  
<style scoped>
.el-header,
.el-footer {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 40px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

body>.el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
</style>