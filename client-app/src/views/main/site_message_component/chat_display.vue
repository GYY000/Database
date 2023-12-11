<template>
  <div class="message-container" ref="container" style="height: 85%;">
    <div v-if="messages.length == 0 && messageLoaded" style="margin-top: 30px;font-size: 20px;"> 你们还没有过聊天记录 </div>
    <div style="display: flex; justify-content: center; align-items: center" v-if="!messageLoaded">
      <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
        x="0px" y="0px" width="24px" height="30px" viewBox="0 0 24 30" style="enable-background:new 0 0 50 50;"
        xml:space="preserve">
        <rect x="0" y="13" width="4" height="5" fill="#333">
          <animate attributeName="height" attributeType="XML" values="5;21;5" begin="0s" dur="0.6s"
            repeatCount="indefinite" />
          <animate attributeName="y" attributeType="XML" values="13; 5; 13" begin="0s" dur="0.6s"
            repeatCount="indefinite" />
        </rect>
        <rect x="10" y="13" width="4" height="5" fill="#333">
          <animate attributeName="height" attributeType="XML" values="5;21;5" begin="0.15s" dur="0.6s"
            repeatCount="indefinite" />
          <animate attributeName="y" attributeType="XML" values="13; 5; 13" begin="0.15s" dur="0.6s"
            repeatCount="indefinite" />
        </rect>
        <rect x="20" y="13" width="4" height="5" fill="#333">
          <animate attributeName="height" attributeType="XML" values="5;21;5" begin="0.3s" dur="0.6s"
            repeatCount="indefinite" />
          <animate attributeName="y" attributeType="XML" values="13; 5; 13" begin="0.3s" dur="0.6s"
            repeatCount="indefinite" />
        </rect>
      </svg>
      <span style="margin-left: 10px;">加载中...</span>
    </div>
    <div v-for="message in messages" :key="message.id">
      <div v-if="message.is_sender" class="message-right">
        <div style="display: flex;flex-direction: column;   align-items: flex-end; justify-content: flex-end;">
          <div class="time">{{ message.time }}</div>
          <div class="content">
            {{ message.content }}
          </div>
        </div>
        <img :src="my.profile_photo" alt="头像" class="profile-photo" />
      </div>
      <div v-else class="message-left">
        <img :src="this.op_profile_photo" alt="头像" class="profile-photo" />
        <div style="display: flex;flex-direction: column;   align-items: flex-start; justify-content: flex-start;">
          <div class="time">{{ message.time }}</div>
          <div class="content">
            {{ message.content }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

  
<script>
import axios from 'axios';
import userStateStore from "@/store";
export default {
  props: {
    contact: {
      type: Object,
      required: true,
    },
  },
  data() {
    const store = userStateStore()
    return {
      op_profile_photo: '/src/assets/image/default-avatar.png',
      messages: [],
      my: {
        "id": store.getUserId,
        "profile_photo": store.getProfilePhoto
      },
      messageLoaded: false,

    };
  },
  mounted() {
    console.log("mounted钩子启动")
    this.messageLoaded = false;
    this.getProfilePhoto();
    this.getMessages();
    this.updateData();
  },
  watch: {
    contact: function (oldVal, newVal) {
      console.log("watch钩子启动")
      this.stopTimer();
      this.messages = []
      this.$nextTick(() => {
        this.getMessages();
        this.getProfilePhoto();
        this.updateData();
      })
    }
  },
  methods: {
    getProfilePhoto() {
      axios.post('/get_profile_photo', { user_name: this.contact.user_name })
        .then(response => {
          if (response.data.profile_photo) {
            this.op_profile_photo = response.data.profile_photo;
            this.op_profile_photo = this.op_profile_photo.startsWith('/9j') ? 'data:image/jpg;base64,' + this.op_profile_photo : 'data:image/png;base64,' + this.op_profile_photo
          }
        })
        .catch(error => {
          console.error(error);
        });
    },

    getMessages() {
      const store = userStateStore()
      axios.post('/get_history_message', { receiver: this.contact.user_id, sender: store.getUserId })
        .then(response => {
          this.messageLoaded = true;
          if (response.data.receiver == this.contact.user_id && response.data.message_list.length > this.messages.length) {
            const diff = response.data.message_list.length - this.messages.length;
            this.messages.push(...response.data.message_list.slice(-diff));
            this.scrollToBottom();
          }
        })
        .catch(error => {
          console.error(error);
        });
    },

    updateData() {
      this.timer = setInterval(() => {
        // 在回调函数中执行需要定时更新的操作
        this.getMessages();
      }, 1000); // 每隔5秒钟执行一次
    },

    stopTimer() {
      if (this.timer) {
        clearInterval(this.timer);
      }
    },

    scrollToBottom() {
      var container = this.$refs.container;
      if (container) {
        this.$nextTick(() => {
          container.scrollTop = container.scrollHeight;
          console.log("移动到最下！", container.scrollHeight, container.scrollTop)
        });
      }
    }
  },
};
</script>


<style scoped>
.message-container {
  /* 可根据实际需要设置高度 */
  height: 420px;
  line-height: 1.5;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
  padding-bottom: 70px;
}

.message-right {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-end;
  text-align: left;
}

.message-left {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  text-align: left;
}

.content {
  background-color: antiquewhite;
  padding: 5px;
  border-radius: 10px;
  font-weight: bold;
  word-wrap: break-word;
  max-width: 400px;
}

.profile-photo {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 50%;
}

.time {
  font-size: 12px;
  /* 字体变小 */
  color: #999;
  /* 颜色变淡 */
  margin-top: 5px;
}
</style>