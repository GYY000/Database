<template>
   <el-dialog v-model="confirmVisible" title="Warning" width="30%" center>
    <span>
      你确定要删除这条评论吗
    </span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="confirmVisible = false">Cancel</el-button>
        <el-button type="primary" @click="deleteComment">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-card class="box-card">
    <div class="comment-header el-card__header">
      <img :src="profile_photo" alt="头像" class="profile-photo" />
      <h2>{{ comment.user_name }}</h2>
    </div>
    <!--<p class="content">{{ comment.content }}</p>-->
    <v-md-preview :text="comment.content" class="content"></v-md-preview>
    <el-button plain v-if="deletable" class="delete-button" @click="confirmVisible=true, confirmMessage='你确定要删除这条评论吗'">
      <el-icon style="color:brown;"><CloseBold /></el-icon>
    </el-button>
    <p class="update-time">{{ comment.create_time }}</p> <!-- 更新时间放在右下角 -->
  </el-card>
</template>
    
<script>
import axios from 'axios';
import { ref } from "vue";
export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
    deletable: {
      type: Boolean,
      required: true,
    }
  },
  data() {
    return {
      profile_photo: '/src/assets/image/default-avatar.png', // 使用本地变量存储post对象
    };
  },
  setup() {
    const confirmVisible = ref(false);
    return {
      confirmVisible,
    }
  },
  mounted() {
    this.getProfilePhoto();
  },
  methods: {
    deleteComment() {
      this.confirmVisible = false;
      axios.post(`/delete_comment`, {cid:this.comment.cid})
        .then((response) => {
          this.$router.go(0);
        })
        .catch(error => {
          console.error(error)
        })
    },
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
  height: 80px;
}

.placeholder {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #ddd;
}

.profile-photo {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 50%;
}

.box-card {
  border-radius: 3px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  height: auto;
}

.update-time {
  position: absolute;
  bottom: 8px;
  /* 距离底部10px */
  right: 10px;
  /* 距离右侧10px */
  font-size: 12px;
  /* 字体变小 */
  color: #999;
  margin-bottom: 5px;
  /* 颜色变淡 */
}

.delete-button {
  position: absolute;
  right: 10px; 
  bottom: 30px;
  width: 15px;
  height: 25px;
  color: brown;
}
</style>