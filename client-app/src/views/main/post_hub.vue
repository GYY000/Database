<template>
    <div>
      <h1>帖子列表</h1>
      <post v-for="post in posts" :key="post.pid" :post="post" />
      <div class="pagination">
        <button @click="loadPage(pageNo - 1)" :disabled="pageNo === 1">上一页</button>
        <button v-for="page in totalPages" :key="page" @click="loadPage(page)" :class="{ active: page === pageNo }">{{ page }}</button>
        <button @click="loadPage(pageNo + 1)" :disabled="pageNo === totalPages">下一页</button>
      </div>
    </div>
  </template>
    
  <script>
  import post from "@/views/main/post_component/post.vue";
  import axios from 'axios';
  
  export default {
    name: "post_hub",
    components: {
      post
    },
    data() {
      return {
        posts: [],
        pageNo: 1,
        pageSize: 5,
        totalPosts: 0
      };
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
  