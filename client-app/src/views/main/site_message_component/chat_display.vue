<template>
  <div class="message-container">
    <div v-for="message in messages" :key="message.id">
      <div v-if="message.sender_id == my.id" class="message-right">
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
    };
  },
  mounted() {
    this.getProfilePhoto();
    this.getMessages();
    this.updateData();
  },
  beforeDestroy() {
    console.log(destroyed)
    clearInterval(this.timer);
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
      axios.post('/get_history_message', { uid1: this.contact.user_id, uid2: store.getUserId })
        .then(response => {
          this.messages = response.data
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
    }
  },
};
</script>


<style scoped>
.message-container {
  /* 可根据实际需要设置高度 */
  height: auto;
  line-height: 1.5;

  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto; /* 当消息过多时添加滚动条 */
  padding-bottom: 60px; /* 设置底部留白 */
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
  max-width: 60%;
}

.profile-photo {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 50%;
}

.time {
  font-size: 12px; /* 字体变小 */
  color: #999; /* 颜色变淡 */
  margin-top: 5px;
}
</style>