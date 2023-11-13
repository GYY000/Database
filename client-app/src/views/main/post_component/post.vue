<template>
  <router-link :to="`/post_detail/${post.pid}`" class="router-link-active">
    <el-card class="box-card">
      <div class="post-header el-card__header">
        <img v-if="profile_photo !== ''" :src="profile_photo" alt="头像" class="profile-photo" />
        <div v-else class="placeholder"></div>
        <h2>{{ post.creator_name }}</h2>
      </div>
      <h3>{{ post.title }}</h3>
      <p class="content">{{ post.content }}</p>
      <p class="update-time">{{ post.update_time }}</p> <!-- 更新时间放在右下角 -->
    </el-card>
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
.placeholder {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #ddd;
}

.post-header {
  display: flex;
  align-items: center;
  height: 80px;
}

.profile-photo {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 50%;
}

.box-card {
  border-radius: 10px; /* 设置圆角 */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
  transition: transform 0.3s, box-shadow 0.3s; /* 添加鼠标交互效果的过渡动画 */
  position: relative; /* 设置为相对定位，以便将更新时间放在右下角 */
  height: 240px;
}

.box-card:hover {
  transform: translateY(-5px); /* 鼠标悬停时的交互效果，可以根据需要自行调整 */
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2); /* 鼠标悬停时的阴影效果，可以根据需要自行调整 */
}

.update-time {
  position: absolute;
  bottom: 10px; /* 距离底部10px */
  right: 10px; /* 距离右侧10px */
  font-size: 12px; /* 字体变小 */
  color: #999; /* 颜色变淡 */
}

.content {
  overflow: hidden; /* 内容超出部分隐藏 */
  text-overflow: ellipsis; /* 超出部分用省略号表示 */
  white-space: nowrap; /* 不换行 */
  max-height: 1.2em; /* 设置最大高度为1行的高度 */
}

a{
  text-decoration: none;
}
.router-link-active {
  text-decoration: none;
}
</style>
