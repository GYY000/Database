<template>
  <router-link :to="`/post_detail/${post.pid}`" class="no-underline">
    <div class="post">
      <img v-if="post.profile_photo" :src="post.profile_photo" alt="头像" />
      <div v-else class="placeholder"></div>
      <h2>{{ post.title }}</h2>
      <p>{{ post.content }}</p>
      <p>作者：{{ post.creator_name }}</p>
      <p>更新时间：{{ post.update_time }}</p>
    </div>
  </router-link>
</template>

<script>
import axios from 'axios';
export default {
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  created() {
    if (this.post.uid) {
      // 发起 POST 请求获取用户的头像信息
      axios.post('/get_profile_photo', { uid: this.post.uid })
        .then(response => {
          this.post.profile_photo = response.data.profile_photo;
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
};
</script>

<style scoped>
.post {
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}

.placeholder {
  width: 100px;
  height: 100px;
  background-color: #ddd;
}
</style>
