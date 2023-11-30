<template>
  <div ref="detailDiv" style="width: 1000px;position:absolute;margin: auto;top: 0;left: 0;bottom: 0;right: 0;height: auto;">
    <el-card class="box-card">
      <div class="card-content">
        <div class="post-header">
          <img :src="profile_photo" alt="头像" class="profile-photo" />
          <h2>{{ post.creator_name }}</h2>
        </div>
        <h3>{{ post.title }}</h3>
        <v-md-preview :text="post.content" ></v-md-preview>
        <p class="update-time">{{ post.update_time }}</p> <!-- 更新时间放在右下角 -->
      </div>
    </el-card>
    <div class="line"></div> <!-- 添加分割线 -->
    <div class="comment-list">
      <comment v-for="comment in comments" :key="comment.cid" :comment="comment" />
    </div>
    <button ref="fixedButton" style="position: fixed;right: calc(50% - 600px); bottom: 5%;">按钮</button>
  </div>
</template>
  
<script>
import comment from "@/views/main/post_component/comment.vue";
import comment_editor from "@/views/main/post_component/comment_editor.vue";
import axios from "axios";

export default {
  name: "post_detail",
  components: {
    comment,
    comment_editor,
  },
  data() {
    return {
      post: {},
      comments: [],
      profile_photo: '/src/assets/image/default-avatar.png',
    };
  },
  mounted() {
    this.fetchPostDetail();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    fetchPostDetail() {
      const pid = this.$route.params.pid;
      axios.get(`/post_detail/${pid}`)
        .then((response) => {
          this.post = response.data.post;
          this.comments = response.data.comment;
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
        })
        .catch((error) => {
          console.error(error);
        });
    },

    handleScroll() {
      return
      const button = this.$refs.fixedButton;
      const detailDiv = this.$refs.detailDiv;
      if (!button) return;

      const rect = button.getBoundingClientRect();
      const offsetBottom = 20; // 设置按钮与屏幕底部的偏移量
      
      const bottom = window.innerHeight - detailDiv.getBoundingClientRect().bottom;
      console.log(detailDiv.getBoundingClientRect().bottom, window.innerHeight)
      //button.style.bottom = `${bottom}px`;
      //button.style.right = `${right}px`;
    }
  },
};
</script>
<style scoped>
.line {
  height: 1px;
  background-color: #ccc;
  margin: 20px 0;
  position: relative;
}

.line::after {
  content: '';
  position: absolute;
  left: -50%;
  right: -50%;
  top: 50%;
  height: 1px;
  background-color: #ccc;
  transform: translateY(-50%);
}

.comment-list {
  display: flex; /* 使用flex布局 */
  flex-direction: column; /* 设置主轴方向为纵向 */
  gap: 20px; /* 设置卡片之间的间距为20px */
}

.placeholder {
  width: 50px;
  height: 50px;
  border-radius: 50%;
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

.box-card {
  border-radius: 10px;
  /* 设置圆角 */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  /* 添加阴影效果 */
  transition: transform 0.3s, box-shadow 0.3s;
  /* 添加鼠标交互效果的过渡动画 */
  position: relative;
  /* 设置为相对定位，以便将更新时间放在右下角 */
  height: auto;
}

.update-time {
  position: absolute;
  bottom: 10px;
  /* 距离底部10px */
  right: 10px;
  /* 距离右侧10px */
  font-size: 12px;
  /* 字体变小 */
  color: #999;
  /* 颜色变淡 */
}
</style>