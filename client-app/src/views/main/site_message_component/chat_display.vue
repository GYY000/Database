<template>
  <div v-for="message in messages" :key="index">
    <!-- 有聊天记录：循环聊天记录 -->
    <div v-if="list.username == userInfo.name">
      <!-- 再循环显示聊天记录 -->
      <p :class="{ 'right': msg.type == 'my' }" v-for="(msg, index) in list.list" :key="index">
        <el-avatar v-if="msg.type == 'user'" :src="userInfo.img"></el-avatar>
        <el-avatar v-if="msg.type == 'my'" :src="myInfo.img" style="float:right;"></el-avatar>
        <span class="content">{{ msg.msg }}</span>
      </p>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
export default {
  props: {
    contact: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      op_profile_photo: '/src/assets/image/default-avatar.png',
      messages: [],
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


<style>
.content{
  background-color: antiquewhite;
  padding: 10px;
  border-radius: 10px;
  font-weight: bold;
}
.right{
  text-align: right;
}
</style>