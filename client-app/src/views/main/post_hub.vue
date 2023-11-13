<template>
  <div>
    <div>
      <h1>{{this.title}}</h1>
      <input type="text" v-model="searchKeyword" placeholder="输入关键字搜索" />
      <button @click="searchPosts">搜索</button>
      <button @click="searchMyPosts">查看我的帖子</button>
      <button @click="loadPosts">查看全部帖子</button>

      <div>
        <el-button type="primary" @click="showDialog">新建帖子</el-button>
        <el-dialog v-model="dialogVisible" title="新建帖子">
          <el-form :model="newPost" label-width="80px">
            <el-form-item label="标题">
              <el-input v-model="newPost.title"></el-input>
            </el-form-item>
            <el-form-item label="内容">
              <el-input type="textarea" v-model="newPost.content"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="savePost">确 定</el-button>
          </div>
        </el-dialog>
      </div>

    </div>
    <div class="post-list">
      <post v-for="post in posts" :key="post.pid" :post="post" />
    </div>
    <div class="pagination">
      <button @click="loadPage(pageNo - 1)" :disabled="pageNo === 1">上一页</button>
      <button v-for="page in totalPages" :key="page" @click="loadPage(page)" :class="{ active: page === pageNo }">{{ page
      }}</button>
      <button @click="loadPage(pageNo + 1)" :disabled="pageNo === totalPages">下一页</button>
    </div>
  </div>
</template>
    
<script>
import post from "@/views/main/post_component/post.vue";
import axios from 'axios';
import {ref} from "vue";
import userStateStore from "@/store";
export default {
  name: "post_hub",
  components: {
    post
  },
  data() {
    return {
      title: "全部帖子",
      posts: [],
      pageNo: 1,
      pageSize: 3,
      totalPosts: 0,
      searchKeyword: '',
      newPost: {}
    };
  },
  setup() {
    const dialogVisible = ref(false);
    return {
      dialogVisible
    }
  },
  mounted() {
    this.loadPosts();
  },
  methods: {
    loadPosts() {
      // 发送 POST 请求，获取帖子数据和总数量
      const requestData = {
        page_no: this.pageNo,
        page_size: this.pageSize
      };

      axios.post('/post_hub', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          this.posts = response.data.posts;
          this.totalPosts = response.data.total;
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
    },
    loadPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.pageNo = page; // 加载指定页码的帖子数据
        this.loadPosts();
      }
    },
    reloadAllPosts() {
      this.pageNo = 1;
      this.loadPosts();
    },
    searchPosts() {
      this.pageNo = 1
      this.posts = []
      const requestData = {
        page_no: this.pageNo,
        page_size: this.pageSize,
        key_word: this.searchKeyword
      };
      axios.post('/search_post', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          this.posts = response.data.posts;
          this.totalPosts = response.data.total;
          this.title = this.searchKeyword + "的搜索结果";
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
    },
    searchMyPosts() {
      this.pageNo = 1
      this.posts = []
      const store = userStateStore();
      const requestData = {
        page_no: this.pageNo,
        page_size: this.pageSize,
        uid: store.getUserId,
      };
      axios.post('/get_user_post', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          this.posts = response.data.posts;
          this.totalPosts = response.data.total;
          this.title = "我的帖子";
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
    },

    showDialog() {
        this.dialogVisible = true;
      },
    savePost() {
        // 这里可以添加保存帖子的逻辑，比如发送到后端API
        console.log('保存帖子', this.post);
        this.dialogVisible = false;
        const store = userStateStore();
        const requestData = {
          title: this.newPost.title,
          content: this.newPost.content,
          uid: store.getUserId,
        };
        axios.post('/create_post', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          console.log(response)
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
      }
    },

  computed: {
    totalPages() {
      return Math.ceil(this.totalPosts / this.pageSize);
    }
  }
};
</script>
<style scoped>
.post-list {
  display: flex;
  /* 使用flex布局 */
  flex-direction: column;
  /* 设置主轴方向为纵向 */
  gap: 20px;
  /* 设置卡片之间的间距为20px */
}

.pagination {
  margin-top: 20px;
}

.pagination button {
  margin-right: 5px;
}

.pagination button.active {
  font-weight: bold;
}
</style>
  