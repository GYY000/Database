<template>
  <div class="comment">
    <div class="comment-header">
      <img v-if="this.profile_photo" :src="this.profile_photo" alt="头像" class="profile-photo"/>
      <div v-else class="placeholder"></div>
      <h2>{{ comment.user_name }}</h2>
    </div>
    <p>{{ comment.content }}</p>
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
      axios.post('/get_profile_photo', { user_name: this.comment.user_name })
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
.comment {
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}

.comment-header {
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
<style scoped></style>