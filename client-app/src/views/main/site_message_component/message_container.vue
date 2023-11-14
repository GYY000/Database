<template>
  <el-container style="height: 600px;">
    <el-container style="height: auto;">
      <el-aside :span="8">
        <h1>
          我的消息 
        </h1>
        <contact v-for="contact in contacts" :key="contact.user_id" :contact="contact" @open-message="handleContactClicked" />
        <div v-if="contacts.length == 0">没有人给你发消息</div>
      </el-aside>
      <el-container>
        <el-main>
          <chat_display v-if="Object.keys(cur_contact).length > 0" :contact="cur_contact"></chat_display>
          <div v-else>暂无</div>
        </el-main>
        <el-footer>
          <el-input placeholder="请输入内容" v-model="this.new_message" @keyup.enter.native="send"> </el-input>
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
      new_message: ''
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
        })
        .catch(error => {
          console.error(error);
      });
    },
    send() {
      const store = userStateStore()
      axios.post('/send_message', { sender_id: store.getUserId, receiver_name: this.cur_contact.user_name, content: this.new_message})
        .then(response => {
          console.log(response)
          this.new_message = ''
          //this.messages.push(response.data)
        })
        .catch(error => {
          console.error(error);
        });
    },
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