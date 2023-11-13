<template>
  <router-link :to="`/post_detail/${post.pid}`" class="no-underline">
    <div class="post">
      <div class="post-header">
        <img v-if="profile_photo !== ''" :src="profile_photo" alt="头像" class="profile-photo" />
        <div v-else class="placeholder"></div>
        <h2>{{ post.title }}</h2>
      </div>
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
  data() {
    return {
      profile_photo: '', // 使用本地变量存储post对象
    };
  },
  mounted() {
    this.getProfilePhoto();
  },
  methods: {
    getProfilePhoto() {
      axios.post('/get_profile_photo', { user_name: this.post.creator_name })
        .then(response => {
          if (response.data.profile_photo) {
            this.profile_photo = response.data.profile_photo;
            this.profile_photo = this.profile_photo.startsWith('/9j') ? 'data:image/jpg;base64,' + this.profile_photo : 'data:image/png;base64,' + this.profile_photo
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

.post-header {
  display: flex;
  align-items: center;
}

.profile-photo {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 50%;
}
</style>
