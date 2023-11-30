<template>
  <el-dialog v-model="dialogVisible" title="回复帖子">
    <el-form :model="newComment" label-width="80px">
      <el-form-item label="内容">
        <mavon-editor class="markdown" :value="newComment.content" v-model="newComment.content"
          :scrollStyle="mavon_config.scrollStyle" :toolbars="mavon_config.toolbars" :subfield="mavon_config.subfield"
          placeholder="请输入内容" style="height: 200px;width: 100%;margin-bottom: 10px" @imgAdd="img_add" />
        <!--<el-input type="textarea" v-model="newPost.content"></el-input>-->
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer" style="display: flex; justify-content: flex-end;">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="saveComment">确 定</el-button>
    </div>
  </el-dialog>

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
    <el-button ref="fixedButton" @click="() => { dialogVisible = true }" style="position: fixed;right: calc(50% - 580px); bottom: 5%; width: 55px;height: 55px;">
      <el-icon :size="30"><Comment /></el-icon>
    </el-button>
  </div>
</template>
  
<script>
import comment from "@/views/main/post_component/comment.vue";
import comment_editor from "@/views/main/post_component/comment_editor.vue";
import { upload_picture } from "@/views/main/api";
import userStateStore from "@/store";
import axios from "axios";
import { ref } from "vue";

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
      newComment: {},
    };
  },
  setup() {
    const dialogVisible = ref(false);
    const mavon_config = ref({
      scrollStyle: true,
      toolbars: {
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: false, // 中划线
        mark: false, // 标记
        superscript: true, // 上角标
        subscript: true, // 下角标
        quote: true, // 引用
        ol: true, // 有序列表
        ul: true, // 无序列表
        link: true, // 链接
        imagelink: true, // 图片链接
        code: true, // code
        table: true, // 表格
        fullscreen: false, // 全屏编辑
        readmodel: false, // 沉浸式阅读
        htmlcode: false, // 展示html源码
        help: false, // 帮助
        undo: true, // 上一步
        redo: true, // 下一步
        trash: true, // 清空
        save: true, // 保存（触发events中的save事件）
        navigation: false, // 导航目录
        alignleft: true, // 左对齐
        aligncenter: true, // 居中
        alignright: true, // 右对齐
        subfield: false, // 单双栏模式
        preview: true, // 预览
      }
    }
    )
    return {
      dialogVisible,
      mavon_config
    }
  },
  mounted() {
    this.fetchPostDetail();
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
    saveComment() {
      // 这里可以添加保存帖子的逻辑，比如发送到后端API
      const store = userStateStore();
      const postData = {
        uid: store.getUserId,
        content: this.newComment.content,
        pid: this.$route.params.pid
      };
      axios.post(`/post_detail/${this.$route.params.pid}`, postData)
        .then(response => {
          this.inputValue = ''
          this.comments.push(response.data)
        })
        .catch(error => {
          console.error('接口请求失败:', error);
        });
      this.dialogVisible = false;
      this.newComment = {}
    },
    img_add(pos, file) {
      let form_data = new FormData
      form_data.append('image', file)
      upload_picture(form_data).then(
        (res) => {
          let content = this.newComment.content
          let name = file.name
          // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)  这里是必须要有的
          if (content.includes(name)) {
            let oStr = `(${pos})`
            let nStr = `(${res.img_url})`
            let index = content.indexOf(oStr)
            let str = content.replace(oStr, '')
            let insertStr = (soure, start, newStr) => {
              return soure.slice(0, start) + newStr + soure.slice(start)
            }
            this.newComment.content = insertStr(str, index, nStr)
          }
        }
      )
    },
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