<template>
    <div class="message-container">
        <!-- 有聊天记录：循环聊天记录 -->
        <div v-if="message.sender_id == my.id" class="message-right">
          <!-- 再循环显示聊天记录 -->
          <p class="content">{{message.content}}</p>
          <img :src="my.profile_photo" alt="头像" class="profile-photo" />
        </div>
        <div v-else class="message-left">
          <img :src="this.op_profile_photo" alt="头像" class="profile-photo" />
          <p class="content">{{message.content}}</p>
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
        messages: [
          {
              "sender_name": "gyy",
              "sender_id": 7,
              "receiver_name": "zhangjue",
              "receiver_id": 8,
              "content": "helloakjhdskfjhkajhkuhlujjjjjjjjjjahelloakjhdskfjhkajhkuhlujjjjjjjjjjahelloakjhdskfjhkajhkuhlujjjjjjjjjjahelloakjhdskfjhkajhkuhlujjjjjjjjjja",
              "time": "123",
              "read": true,
              "id": 1 
          },
          {
              "sender_name": "zhangjue",
              "sender_id": 8,
              "receiver_name": "gyy",
              "receiver_id": 7,
              "content": "hello",
              "time": "123",
              "read": true,
              "id": 1 
          }
        ],
        my: {
          "id": store.getUserId,
          "profile_photo": store.getProfilePhoto
        }
      };
    },
    mounted() {
      this.getProfilePhoto();
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
    },
  };
  </script>
  
  
  <style scoped>
  .message-container {
    /* 可根据实际需要设置高度 */
    height: auto;
    line-height: 1.5;
  }
  
  .message-right {
    text-align: right;
  }
  
  .message-left {
    text-align: left;
  }
  
  .content {
    background-color: antiquewhite;
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
    word-wrap: break-word;
    max-width: 70%;
  }
  
  .profile-photo {
    width: 50px;
    height: 50px;
    object-fit: cover;
    margin-right: 10px;
    border-radius: 50%;
  }
  </style>