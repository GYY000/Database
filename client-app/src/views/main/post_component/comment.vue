<template>
  <div class="comment">
    <h2>{{ comment.user_name }}</h2>
    <p>{{ comment.content }}</p>
    <img v-if="comment.profile_photo" :src="comment.profile_photo" alt="头像" />
    <div v-else class="placeholder"></div>
  </div>
</template>
    
  <script>
  import axios from 'axios';
export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
  },
  created() {
    if (this.comment.uid) {
      // 发起 POST 请求获取用户的头像信息
      axios.post('/get_profile_photo', { uid: this.comment.uid })
        .then(response => {
          this.comment.profile_photo = response.data.profile_photo;
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
};
</script>
    
  <style scoped>
.comment {
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}
</style>
<style scoped></style>